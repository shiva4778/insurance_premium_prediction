FROM python:3.7.0-alpine  
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

CMD python app.py
