# Team Directory API

Team Directory API is a FastAPI service for adding team members, listing all members, and filtering members by team. Each member has a generated `id`, a `name`, a `team`, and a `role`. SQLAlchemy stores the records in SQLite. The app creates `team_directory.db` in the working directory on startup if it does not exist.

## Install on Windows

Install Python 3 with the Windows Python launcher (`py`). In PowerShell, open the project folder and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

These commands use the virtual environment directly; no activation is needed.

## Run on Port 8020

From the project folder in PowerShell, run:

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --port 8020
```

Open [Swagger UI](http://127.0.0.1:8020/docs). Press `Ctrl+C` in PowerShell to stop the server.

## Endpoints

| Method | Path | Status codes |
| --- | --- | --- |
| `POST` | `/team/` | `201 Created`: member with a generated `id`; `422 Unprocessable Entity`: invalid or missing request body. |
| `GET` | `/team/` | `200 OK`: all members, or `[]` if the directory is empty. |
| `GET` | `/team/by-team/{team_name}` | `200 OK`: members whose team exactly matches `team_name`; `404 Not Found`: no matching members; `422 Unprocessable Entity`: invalid path parameter. |

## Test Manually in Swagger UI

There is no automated test suite yet. With the server running, open Swagger UI and expand the `team` endpoints. For each request, select **Try it out**, enter any required input, select **Execute**, and check the response status and body.

1. **Create a member:** In `POST /team/`, submit the JSON below. Expect `201` and a response containing the submitted fields plus an integer `id`. This creates a record in the local database.

   ```json
   {
     "name": "Alex Rivera",
     "team": "Platform",
     "role": "Engineer"
   }
   ```

2. **List all members:** Execute `GET /team/`. Expect `200` and an array containing the member you just created.
3. **Filter by team:** In `GET /team/by-team/{team_name}`, enter `Platform`. Expect `200` and an array containing the new member and any other members on that team, but none from other teams.
4. **Check a missing team:** Repeat the team lookup with a name you haven't used, such as `NoSuchTeam`. Expect `404` and `{"detail":"No members found for this team"}`.
5. **Check request validation:** Repeat `POST /team/` with `role` removed from the JSON. Expect `422` and a validation error identifying the missing field.