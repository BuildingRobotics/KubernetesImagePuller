FROM python:2.7

WORKDIR /deploy

RUN adduser --system --uid 500 --group controller

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY controller.py .

USER controller

CMD ["python", "controller.py"]
