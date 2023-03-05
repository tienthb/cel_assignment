FROM python:3.8.10

WORKDIR /app

COPY src/fastapi_app/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY src/fastapi_app/ /app/fastapi_app/

ENTRYPOINT ["uvicorn", "fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

EXPOSE 8000