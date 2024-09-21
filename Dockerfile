# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install the app dependencies using Poetry
RUN poetry install --no-dev

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "happiness-app.py", "--server.port=8501", "--server.address=0.0.0.0"]
