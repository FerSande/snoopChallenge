FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./requirements.txt
COPY employeeApp.py ./employeeApp.py
COPY apiEmployee.py ./apiEmployee.py
COPY settings.py ./settings.py


RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python","/apiEmployee.py"]

