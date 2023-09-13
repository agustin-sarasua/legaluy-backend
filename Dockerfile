FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app/

# Install dependencies
RUN pip install -r requirements.txt

# # Expose port
EXPOSE 8000
# Start application with Uvicorn
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000


