FROM python:3.8.12

WORKDIR /api

COPY requirements.txt .
COPY main.py .
COPY utils.py .

RUN pip install -r requirements.txt


EXPOSE 80
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]