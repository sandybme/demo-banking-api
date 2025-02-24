# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /banking_api

# Copy the application code
COPY . /banking_api

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000
EXPOSE 8501

# Run the FastAPI application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run front-end.py --server.port=8501 --server.address=0.0.0.0"]


