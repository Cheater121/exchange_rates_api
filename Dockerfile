FROM python:3.10

RUN mkdir /exchange_rates_api

WORKDIR /exchange_rates_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

RUN curl -o docker/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh

RUN chmod +x docker/wait-for-it.sh 

# EXPOSE 80
