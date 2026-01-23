from fastapi import FastAPI, status, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import uuid
from pydantic_schema import Tweety, Tweety_update

app = FastAPI()


# load all-tweets.
def load_tweets():
    with open("tweety.json", "r") as file:
        result = json.load(file)
    return result


# save tweets in json file.
def save_tweets(data):
    with open("tweety.json", "w") as file:
        json.dump(data, file)


# access all tweets
@app.get("/tweets")
def get_all_tweets():
    data = load_tweets()
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)


# sort tweets by username
@app.get("/tweets/sort")
def sorted_tweets(
    sort_by: str = Query(
        title="get tweets base on username",
        description="enter username to access his all tweets",
    )
):
    tweets = load_tweets()
    usernames = []
    for tweet in tweets:
        usernames.append(tweet["username"])

    if sort_by not in usernames:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="no content for this user provide a valid user👻",
        )
    else:
        for tweet in tweets:
            if sort_by == tweet["username"]:
                yield {"tweet": tweet["content"]}


# create a new tweet
@app.post("/tweets/create")
def create_tweet(tweet_data: Tweety):
    data = load_tweets()
    tweet_id = str(uuid.uuid4())
    new_tweet = Tweety(
        id=tweet_id, username=tweet_data.username, content=tweet_data.content
    )
    tweet_dict = new_tweet.model_dump()
    data.append(tweet_dict)
    save_tweets(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content="tweet created successfully"
    )


#  update tweet by id
@app.put("/tweets/{tweet_id}/update")
def update_tweet(tweet_id: str, update_data: Tweety_update):
    all_tweets = load_tweets()
    updated = False
    for idx, tweet in enumerate(all_tweets):
        if tweet["id"] == tweet_id:
            updated_tweet = update_data.model_dump(exclude_unset=True)
            for k, v in updated_tweet.items():
                tweet[k] = v
            all_tweets[idx] = tweet
            updated = True
            break

    if updated == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid id: {tweet_id}  ,cant update tweet enter the valid id please.",
        )
    save_tweets(all_tweets)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"tweet: {tweet_id} updated successfully👻",
    )


# delete tweet by id
@app.delete("/tweets/{id}/delete")
def delete_tweets(id: str):
    tweets = load_tweets()
    is_deleted = False
    for idx, tweet in enumerate(tweets):
        if tweet["id"] == id:
            del tweets[idx]
            is_deleted = True
            break

    if is_deleted == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"invalid id: {id}  ,cant delete tweet enter the valid id please.",
        )
    save_tweets(tweets)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=f"tweet: {id} deleted successfully👻",
    )
