# panda-crud

A CRUD backend API built in Python with the [FastAPI](https://fastapi.tiangolo.com/) framework.

The application handles patient demographic data, addresses, and appointments.

## Installation Instructions

### Via Pip/Python

Install the dependancies:

```
pip install -r requirements.txt
```

Run via uvicorn:

```
uvicorn panda.main:app
```

### Via Docker

Build the Docker image:

```
docker build -t panda .
```

Run Docker image:

```
docker run -d -p 80:80 panda
```

## Access CRUD

### Local

[https://127.0.0.1](https://127.0.0.1) (Depending on local setup)

### Hosted Version

[https://pandacrud-1-r3693083.deta.app](https://pandacrud-1-r3693083.deta.app) (Only allows GET actions)

## Docs

Access OpenAPI docs via [URL]/docs, or Redoc via /redoc.

Example payloads are included for patients, addresses and appointments in the OpenAPI docs.

## Validators

### Model Field Validation

FastAPI/Pydantic take care of a lot of the validation and error reporting for missing/invalid requests.

They also take care of serialising/deserialising objects in requests and responses, and automatic type conversion - helping to avoid errors/mistakes in the code.

We can also add our own validator methods with decorators. For example, using RegEx to check a valid postcode, to check a datetime has timezone data, or that the appointment end_at field is after the start_at field.

### NHS Number Validation

Validation is done via [is_valid_nhs_number](panda/util/nhs_validator.py). The NHS Number is checked via Pydantic's validator decorator. ValueError is raised and returned to the user if the payload number fails this check.

## Testing

Basic examples of unit tests are included in [/tests](/tests). These are performed with pytest. Fixtures are included which provide valid/invalid/badly formatted NHS Numbers, valid and invalid PatientCreate objects, etc.

## Database

The database currently uses SQLite for the MVP but FastAPI can easily integrate with any database supported by SQLAlchemy, e.g., PostgreSQL, MySQL. Migrations need to be enacted with a third-party tool, like Alembic.

## Additional Thoughts and Considerations

Addresses have an owner_type and owner_id field. This allows us to use the Address table to add patient addresses, locations, departments, etc. We can then get the corresponding address record based on these two fields. This avoids having different tables for different address types.

Once appointments have Clinician, Department, etc data (which are currently commented out in the model), we can obtain stats for per-clinicia/department missed appointments. 'Missed' is not currently a field as it can be inferred from the data (is_cancelled = false and attended_at = None).

Foreign markets would require different validation than NHS Numbers. Instead of an NHS Number field, a 'Reference Number' field could be used and a specific validator injected depending on the market.

A more RESTful design -

Given more time, responses would include additional metadata, links, and requests accept an 'include' parameter.

An example response could look like:

```
{
	"data": [
	{
		"id": 1,
		"name": "David Winch",
		...
		"links": [
		{
			"rel": "self",
			"uri": "/patients/1"
		},
		{
			"rel": "patient.address",
			"uri": "/patients/1/address"
		},
		{
			"rel": "patient.appointments",
			"uri": "/patients/1/appointments"
		}
	},
	...
	]
	"pagination": {
		"total": 1000,
		"count": 12,
		"per_page": 12,
		"current_offset": 12,
		"total_pages": 84,
		"next_url": "/patients?offset=12&limit=12"
	}
}
```

## To Do

Testing. Testing. Testing. The tests are there as examples, much more was required before writing the code. In the interest of time, not everything has been tested.

Add fields to models. Patient is missing phone number, email, etc. Pretty important data!

Add Clinician and Department models.

Add functions to get missed appointments, cancelled appointments, etc.

Behaviour testing to test functionality with scenarios, rather than unit testing which may not work as expected.

Remove Address router file - Addresses are attached to a resource. We can get them via the resource path, e.g. /patient/1/address.

Allow queries for requests, beyond just limit and offset.

Index database columns.

Better documentation explanations/examples. E.g., AddressOwnerType in Schema - What is it? What are potential values?

## Endpoints

### [addresses](https://pandacrud-1-r3693083.deta.app/docs#/addresses)

**GET**[/addresses/](https://pandacrud-1-r3693083.deta.app/docs#/addresses/get_addresses_addresses__get) Get Addresses

**GET**[/addresses/{address_id}](https://pandacrud-1-r3693083.deta.app/docs#/addresses/get_address_addresses__address_id__get) Get Address

### [patients](https://pandacrud-1-r3693083.deta.app/docs#/patients)

**GET**[/patients/](https://pandacrud-1-r3693083.deta.app/docs#/patients/get_patients_patients__get) Get Patients

**POST**[/patients/](https://pandacrud-1-r3693083.deta.app/docs#/patients/create_patient_patients__post) Create Patient

**GET**[/patients/getbynhsnumber](https://pandacrud-1-r3693083.deta.app/docs#/patients/get_patient_by_nhs_number_patients_getbynhsnumber_get) Get Patient By Nhs Number

**GET**[/patients/{patient_id}](https://pandacrud-1-r3693083.deta.app/docs#/patients/get_patient_patients__patient_id__get) Get Patient

**PUT**[/patients/{patient_id}](https://pandacrud-1-r3693083.deta.app/docs#/patients/update_patient_patients__patient_id__put) Update Patient

**DELETE**[/patients/{patient_id}](https://pandacrud-1-r3693083.deta.app/docs#/patients/delete_patient_patients__patient_id__delete) Delete Patient

**GET**[/patients/{patient_id}/address](https://pandacrud-1-r3693083.deta.app/docs#/patients/get_patient_address_patients__patient_id__address_get) Get Patient Address

**POST**[/patients/{patient_id}/address](https://pandacrud-1-r3693083.deta.app/docs#/patients/create_patient_address_patients__patient_id__address_post) Create Patient Address

### [appointments](https://pandacrud-1-r3693083.deta.app/docs#/appointments)

**GET**[/appointments/](https://pandacrud-1-r3693083.deta.app/docs#/appointments/get_appointments_appointments__get) Get Appointments

**POST**[/appointments/](https://pandacrud-1-r3693083.deta.app/docs#/appointments/create_appointment_appointments__post) Create Appointment

**GET**[/appointments/{appointment_id}](https://pandacrud-1-r3693083.deta.app/docs#/appointments/get_appointment_by_id_appointments__appointment_id__get) Get Appointment By Id

**PUT**[/appointments/{appointment_id}](https://pandacrud-1-r3693083.deta.app/docs#/appointments/update_appointment_appointments__appointment_id__put) Update Appointment

**POST**[/appointments/{appointment_id}/cancel](https://pandacrud-1-r3693083.deta.app/docs#/appointments/cancel_appointment_appointments__appointment_id__cancel_post) Cancel Appointment

**POST**[/appointments/{appointment_id}/attended](https://pandacrud-1-r3693083.deta.app/docs#/appointments/mark_appointment_attended_appointments__appointment_id__attended_post) Mark Appointment Attended
