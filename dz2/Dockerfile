FROM python:3.12-alpine
RUN pip install fastapi[standard]
WORKDIR /app
COPY main.py /app
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
