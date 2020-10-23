FROM python:3.6
WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000

ENTRYPOINT ["python","app.py"]
CMD ["flask db init","flask db migrate","flask db upgrade"]