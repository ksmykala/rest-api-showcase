FROM python:3.10-slim
WORKDIR /app
RUN mkdir logs
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entrypoint.sh"]