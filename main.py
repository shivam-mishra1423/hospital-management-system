from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Patient(BaseModel):
    id: Annotated[
        str,
        Field(..., description="ID of the patient", examples=["P001"])
    ]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[
        Literal["male", "female", "others"],
        Field(..., description="Gender of the patient")
    ]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[
        Optional[Literal['male', 'female', 'others']],
        Field(default=None)
    ]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    try:
        with open('patients.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f, indent=2)


@app.get('/')
def hello():
    return {'message': 'Patient Management System API'}


@app.get('/about')
def about():
    return {'message': 'A fully Functional API to manage your patient records'}


@app.get('/view')
def view():
    data = load_data()
    return data


@app.get('/patient/{patient_id}')
def view_patient(
    patient_id: str = Path(..., description='Id of the patient in the DB, example = P001')
):
    data = load_data()
    if patient_id in data:
        patient_data = data[patient_id]
        patient_data['id'] = patient_id
        patient = Patient(**patient_data)
        return patient.model_dump()
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(..., description='sort on the basis of height, weight or bmi'),
    order: str = Query('asc', description='sort in asc or desc order')
):
    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field. Select from {valid_fields}')

    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Invalid order. Select between 'asc' and 'desc'")

    data = load_data()
    patients = []

    for pid, pdata in data.items():
        patient_data = pdata.copy()
        patient_data['id'] = pid
        patient = Patient(**patient_data)
        record = patient.model_dump()
        patients.append(record)

    reverse = True if order == 'desc' else False
    return sorted(patients, key=lambda x: x[sort_by], reverse=reverse)


@app.post('/create')
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # Store without id in the JSON file
    patient_dict = patient.model_dump()
    patient_id = patient_dict.pop('id')
    
    data[patient_id] = patient_dict
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={'message': 'patient created successfully'}
    )
    
    
@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    existing_patient_info = data[patient_id]
    
    # Get only the fields that are being updated
    updated_patient_info = patient_update.model_dump(exclude_unset=True)
    
    # Update only the provided fields
    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value
    
    # Create a complete patient object to calculate bmi and verdict
    patient_data_for_validation = existing_patient_info.copy()
    patient_data_for_validation['id'] = patient_id
    
    # Create Patient object to trigger computed fields
    try:
        patient_obj = Patient(**patient_data_for_validation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Invalid data: {str(e)}')
    
    # Convert back to dict (excluding id for storage)
    updated_data = patient_obj.model_dump(exclude=['id'])
    
    data[patient_id] = updated_data
    save_data(data)
    
    return JSONResponse(
        status_code=200, 
        content={'message': 'patient updated successfully'}
    )
    
    
@app.delete('/delete/{patient_id}')
def delete_patient(
    patient_id: str = Path(..., description="ID of the patient to delete, example = P001")
):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Delete patient
    del data[patient_id]
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={"message": f"Patient {patient_id} deleted successfully"}
    )
