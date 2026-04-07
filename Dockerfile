FROM python:3.11-slim

WORKDIR /app

# Copy backend requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy Python entrypoint
COPY backend/entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

# Expose port
EXPOSE 8000

# Use Python entrypoint
CMD ["python3", "/app/entrypoint.py"]
