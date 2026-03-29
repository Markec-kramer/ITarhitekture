FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate gRPC code from proto definition
RUN python generate_proto.py

ENV PYTHONPATH=/app

# gRPC: 50051  |  HTTP + Swagger: 8000
EXPOSE 50051 8000

CMD ["python", "-m", "src.main"]
