FROM python:3.6.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD [ "python3", "./src/gateway.py" ]

ENTRYPOINT ["./entrypoint.sh"]