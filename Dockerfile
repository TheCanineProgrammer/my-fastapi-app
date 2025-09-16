FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Run the FastAPI app
# Match port to the one you will set on Hamravesh/Darkube
CMD ["uvicorn", "First_Scenario:app", "--host", "0.0.0.0", "--port", "8000"]
