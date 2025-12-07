# CRM_FOR-_ALL
[README.md](https://github.com/user-attachments/files/24015896/README.md)
# CRM App

A simple CRM web app for managing cold calling workflows.

## Features

- **Accounts**: Manage company accounts with status tracking.
- **Contacts**: People within accounts, with roles and details.
- **Activities**: Log calls, emails, meetings with outcomes and follow-ups.
- **Follow-ups**: Daily list of contacts to call based on due dates.
- **Dashboard**: Summary of counts and recent activities.
- **Import/Export**: CSV support for accounts and contacts.

## Tech Stack

- Backend: Python + FastAPI, SQLAlchemy, SQLite
- Frontend: React + TypeScript, Axios for API calls

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- pip and npm

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd crm-app/backend
   ```

2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - On Linux/Mac: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

4. Install dependencies:
   ```
   pip install fastapi uvicorn sqlalchemy alembic pandas
   ```

5. Run the backend server:
   ```
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd crm-app/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```
   The app will open at `http://localhost:3000`.

## Usage

- Open the app in your browser.
- Add accounts and contacts.
- Log activities and set follow-ups.
- Check the Follow-ups page for daily tasks.

## API Endpoints

- `/accounts/` - CRUD for accounts
- `/contacts/` - CRUD for contacts
- `/activities/` - CRUD for activities
- `/followups/` - Get follow-up contacts
- `/dashboard/` - Summary data
- `/import/accounts/` - Import accounts CSV
- `/export/accounts/` - Export accounts CSV
- Similar for contacts and activities.

## Assumptions and Notes

- Designed for single user, no authentication.
- SQLite database created automatically.
- CSV import expects columns: for accounts: name, industry, location, status, notes
- For contacts: account_id, name, role_title, department, email, phone, seniority, status
- Basic UI with tables and forms, focus on functionality.
- No advanced features like pagination in UI, but API supports it.

## Development

- Backend uses SQLAlchemy ORM with Pydantic schemas.
- Frontend uses React hooks for state management.
- CORS enabled for localhost:3000.

If you encounter issues with dependencies, ensure Python and Node are properly installed.
