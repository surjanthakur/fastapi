from fastapi import FastAPI, Path, HTTPException, status, Query
from fastapi.responses import JSONResponse
import json
from pydantic_schema import Patient, Patient_update

app = FastAPI()


# load data function.
def load_data():
    with open("patient.json", "r") as data:
        result = json.load(data)
    return result


def save_data(data):
    with open("patient.json", "w") as f:
        json.dump(data, f)


@app.get("/patients")
def get_all_patients():
    data = load_data()
    return {f"all-patients: {data}"}


@app.get("/patients/sort")
def sorting_patients(
    sort_by: str = Query(
        ...,
        title="sort_by must be 'age' or 'weight' ",
        description="enter height or age sort_order to sort patients data",
    ),
    order: str = Query(
        ...,
        title="sorting patients asc. and desc. order",
        description="enter asc. or desc. order to sort patients data",
    ),
):
    valid_fields = ["age", "weight"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="enter valid fields."
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="enter valid order."
        )

    sort_order = True if order == "desc" else False
    response = load_data()
    sorted_data = sorted(
        response.items(),
        key=lambda item: item[1][sort_by],
        reverse=sort_order,
    )
    return [{"patient_id": pid, **data} for pid, data in sorted_data]


@app.get("/patients/{id}")
def get_patient_by_id(
    id: str = Path(
        ...,
        description="this api gives you patient data based on their id",
        max_length=6,
        min_length=4,
        example="p001",
    )
):
    response = load_data()
    if id in response:
        return response[id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="opps!👻 patient not fount 404",
        )


@app.post("/patients/create")
def create_patient(patient_data: Patient):
    response = load_data()

    if patient_data.id in response:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="patient already exist with this id enter another",
        )

    response[patient_data.id] = patient_data.model_dump(exclude=["id"])
    save_data(response)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content="patient created successfully"
    )


@app.put("/patients/{id}/update")
def update_patients(id: str, patient_update: Patient_update):
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalide id plz enter a valid id.",
        )
    existing_patient = data[id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    for key, value in updated_patient_info.items():
        existing_patient[key] = value
    data[id] = existing_patient
    save_data(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"patient {id} updated successfully!"
    )


@app.delete("/patients/{id}/delete")
def delete_patient(id: str):
    data = load_data()
    if id not in data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid patient id enter valid id!",
        )
    del data[id]
    save_data(data)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=f"patient {id} deleted🔻 successfully!"
    )
