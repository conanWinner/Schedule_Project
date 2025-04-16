FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MODEL_PATH=conanWinner/model_scheduler
ENV PORT=5000
ENV HOST=0.0.0.0
ENV DEBUG=False
ENV USE_FP16=True

EXPOSE 5000

CMD ["python", "main.py"]