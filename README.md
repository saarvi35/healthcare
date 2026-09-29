# Healthcare API

This project is a small healthcare backend made with Django and Django REST Framework. It has no website or UI.

Users can create an account and log in. Signed-in users can add and manage their own patients, manage doctors, and assign doctors to patients. The data is saved in PostgreSQL. Login uses JWT tokens.

## Run the project

You need Python and PostgreSQL installed. Create a PostgreSQL database called `healthcare`.

Open PowerShell in this project folder and run:

```powershell
Copy-Item .env.example .env
notepad .env
```

In `.env`, set `DB_PASSWORD` to the password you chose for PostgreSQL. Save the file. Keep `.env` private; it is only for your computer.

Install packages and start the server:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/`. Keep this terminal open while using the API.

## Use the APIs

Use Postman. For requests that need login, choose **Authorization → Bearer Token** and paste the `access` token from login.

### Account

- `POST /api/auth/register/` — create an account with `name`, `email`, and `password`.
- `POST /api/auth/login/` — log in with `email` and `password`. Copy the `access` token from the response.
- `POST /api/auth/token/refresh/` — get a new access token. Send the `refresh` token from login.

### Patients

- `POST /api/patients/` — add a patient. Send `name`, `age`, `gender`, and `address`.
- `GET /api/patients/` — see your patients.
- `GET /api/patients/<id>/` — see one of your patients.
- `PUT /api/patients/<id>/` — update a patient. Send all patient fields.
- `DELETE /api/patients/<id>/` — delete a patient.

### Doctors

- `POST /api/doctors/` — add a doctor. Send `name`, `specialization`, `email`, and `phone`.
- `GET /api/doctors/` — see doctors.
- `GET /api/doctors/<id>/` — see one doctor.
- `PUT /api/doctors/<id>/` — update a doctor. Send all doctor fields.
- `DELETE /api/doctors/<id>/` — delete a doctor.

### Patient and doctor assignments

- `POST /api/mappings/` — assign a doctor to a patient. Send `patient` and `doctor` IDs.
- `GET /api/mappings/` — see your assignments.
- `GET /api/mappings/<patient_id>/` — see the doctors assigned to one of your patients.
- `DELETE /api/mappings/<mapping_id>/` — remove an assignment.

Replace `<id>` with the real ID from an API response. Add your access token to every patient, doctor, and assignment request.
