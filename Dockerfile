FROM python:3.10


ENV PYTHONBUFFERED=1

WORKDIR /code

COPY sfc_tool/requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

EXPOSE 7800