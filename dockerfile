FROM python:3.8

# Set the working directory
WORKDIR /app

# Create a log folder
RUN mkdir /app/log

# Create an empty log file inside the log folder
RUN touch /app/log/app.log

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

