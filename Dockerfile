FROM python:3.12-slim
WORKDIR /app
COPY . /app
EXPOSE 8004
CMD ["python3", "src/server.py"]
