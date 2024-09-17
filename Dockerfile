FROM python:3
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN chmod +x ./start_api.sh
ENTRYPOINT [ "sh", "./start_api.sh" ]