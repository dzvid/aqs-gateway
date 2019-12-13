FROM python:3.5.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/dtn-to-http.py .

COPY entrypoint.sh ./
RUN chmod +x entrypoint.sh

CMD [ "python", "dtn-to-http.py" ]

ENTRYPOINT ["./entrypoint.sh"]