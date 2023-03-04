FROM python:3.8.10

WORKDIR /app

COPY src/streamlit_app/requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY src/streamlit_app/ /app/

ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

EXPOSE 8501