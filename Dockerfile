FROM python:3.8.10

WORKDIR /LB1

COPY func.py main.py ./

CMD ["python","main.py"]