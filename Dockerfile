# Use the full official Python image which includes all necessary build tools
FROM python:3.11

# Install the system libraries needed for lxml
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libxml2-dev \
    libxslt1-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Upgrade Python's build tools first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container
COPY . .

# Tell Render how to run the app. It will automatically use the correct port.
CMD gunicorn --bind 0.0.0.0:$PORT app:app
