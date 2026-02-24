FROM python:3.12-alpine
COPY app/ /app/
WORKDIR /app
EXPOSE 8000
RUN pip install poetry && poetry install
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]