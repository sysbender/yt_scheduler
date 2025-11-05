FROM python:3.11-slim

WORKDIR /data

# Install FlaskCode from PyPI
RUN pip install --no-cache-dir flask flaskcode

# Mount shared folder
VOLUME ["/data"]

# Set RESOURCE_BASEPATH to /data
ENV RESOURCE_BASEPATH=/data

EXPOSE 5001

CMD ["flaskcode",  "/data"]
