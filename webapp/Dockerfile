FROM python:2

EXPOSE 5000
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app .
CMD ["python", "./main.py", "runserver", "-h", "0.0.0.0", "-p", "5000"]