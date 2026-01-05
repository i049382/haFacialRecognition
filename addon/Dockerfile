ARG BUILD_FROM
FROM ${BUILD_FROM}

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    sqlite \
    && pip3 install --no-cache-dir --upgrade pip

# Copy requirements
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app/

# Run the application
CMD ["python3", "-m", "face_recognition_addon"]

