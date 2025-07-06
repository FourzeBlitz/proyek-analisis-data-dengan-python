FROM python:3.9-slim

WORKDIR /app

# Install dependencies globally (no multi-stage needed for small apps)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY Dashboard/ .

# Expose the port and run the application
EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]
