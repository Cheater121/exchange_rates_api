FROM python:3.10

RUN mkdir /exchange_rates_api

WORKDIR /exchange_rates_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

# EXPOSE 80
