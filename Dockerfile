FROM python:3.11-alpine

RUN  mkdir /src

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . .

WORKDIR app

#EXPOSE 5050

CMD ["uvicorn", "routes:app", "--host", "0.0.0.0"]

