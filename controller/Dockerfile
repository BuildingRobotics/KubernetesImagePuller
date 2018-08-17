FROM python:2.7

WORKDIR /deploy

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY controller.py .

CMD ["python", "controller.py"]
