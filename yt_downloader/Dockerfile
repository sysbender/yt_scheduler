FROM python:3.11-slim

WORKDIR /app

# Copy your downloader script and requirements
COPY yt_downloader.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV MAX_PER_DAY=5
ENV DELAY_HOURS=4


# /data will be mounted from host
VOLUME /data

CMD ["python", "yt_downloader.py"]




 
