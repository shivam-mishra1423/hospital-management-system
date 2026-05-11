# Hospital Management System

A simple patient management application built with FastAPI for the backend and a static HTML/JavaScript frontend.

## Project Overview

This project allows you to:
- Add, view, update, and delete patient records.
- Calculate BMI automatically from height and weight.
- Display patient health verdicts like Underweight, Normal, Overweight, and Obese.
- Sort patients by height, weight, or BMI.

The backend is implemented in `main.py` using FastAPI, and the frontend is served from `static/index.html`.

## Features

- REST API endpoints for patient management.
- Browser-based frontend for easy interaction.
- Local JSON storage in `patients.json`.
- Height input in feet on the frontend, converted to meters before BMI calculation.
- CORS support to allow frontend and backend communication.

## How to Run Locally

1. Create a Python virtual environment and activate it.
   ```bash
   python -m venv myenv
   myenv\Scripts\activate
   ```

2. Install dependencies.
   ```bash
   pip install -r requirements.txt
   ```

3. Start the FastAPI server.
   ```bash
   uvicorn main:app --reload
   ```

4. Open the frontend in your browser:
   ```text
   http://127.0.0.1:8000/static/index.html
   ```

## API Endpoints

- `GET /` - Root health check returning a welcome message.
- `GET /about` - About the API.
- `GET /view` - Returns all patients.
- `GET /patient/{patient_id}` - Returns one patient by ID.
- `GET /sort?sort_by=<field>&order=<asc|desc>` - Sort patients by `height`, `weight`, or `bmi`.
- `POST /create` - Create a new patient.
- `PUT /edit/{patient_id}` - Update an existing patient.
- `DELETE /delete/{patient_id}` - Delete a patient.

## File Structure

- `main.py` - FastAPI application and API route definitions.
- `patients.json` - Local JSON database file for patient records.
- `static/index.html` - Frontend UI for interacting with the API.
- `README.md` - Project documentation.
- `requirements.txt` - Python dependencies.
- `.gitignore` - Files and folders ignored by git.

## Notes

- The frontend converts height from feet to meters before sending data to the backend.
- Patient BMI and verdict are calculated server-side in the `Patient` model.
- Do not commit your virtual environment or editor-specific files.

## GitHub Push Instructions

1. Initialize the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: hospital management system"
   ```

2. Create a new GitHub repository manually or with GitHub CLI.

3. Add the remote origin and push:
   ```bash
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git branch -M main
   git push -u origin main
   ```

If you use GitHub CLI:
```bash
gh repo create <repo-name> --public --source=. --remote=origin --push
```
