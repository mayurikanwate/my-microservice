# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the application
CMD ["python", "src/main.py"]
