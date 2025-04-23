FROM python:3.12.10-slim

# Tăng tốc độ và giảm size khi cài gói hệ thống
ENV DEBIAN_FRONTEND=noninteractive


WORKDIR /code

# Cài các phụ thuộc hệ thống cần thiết (nếu cần thêm có thể mở rộng)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements riêng để tối ưu cache layer
COPY app/requirements.txt ./app/requirements.txt


RUN pip install --no-cache-dir -r ./app/requirements.txt


COPY app/ ./app/
#COPY .env .
#docker run --env-file .env -p 8001:8001 schedule_be_nsgaii:v4


ENV PYTHONPATH=/code


EXPOSE 8001


CMD ["python", "-m", "app.main"]
