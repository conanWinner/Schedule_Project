FROM python:3.12.10

WORKDIR /code

COPY .env .
COPY app/ ./app/

RUN pip install --no-cache-dir -r ./app/requirements.txt

# Đảm bảo app là module trong PYTHONPATH
ENV PYTHONPATH=/code

EXPOSE 8001

CMD ["python", "-m", "app.main"]
