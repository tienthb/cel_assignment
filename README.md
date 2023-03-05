# CEL Assignment

## For building and running the application you need:
- [Python 3.8.10](https://www.python.org/downloads/release/python-3810/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/)

## How to use
### To run the application locally

#### Option 1: Run the application in docker
Required: docker-compose is installed in your machine. If not, refer to this page for [Docker Compose Installation] (https://docs.docker.com/compose/install/)

1. Run this command: `docker-compose up --build`
2. Open browser: `http://localhost:8501`

#### Option 2: Run the application in virtualenv

1. Activate virtualenv: `.\venv\Scripts\Activate.ps1` (for Windows machine)
2. Install python packages: `pip install -r requirements.txt`
3. Run this command to start streamlit: `streamlit run .\src\streamlit_app\main.py`
4. Open another terminal in virtualenv and run this command: `uvicorn src.fastapi_app.main:app --reload`
5. Open browser: `http://localhost:8501`