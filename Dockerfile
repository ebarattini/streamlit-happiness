# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the dependency files first to leverage Docker's layer caching
COPY pyproject.toml poetry.lock /app/

# Install Poetry
RUN pip install poetry

# Install the app dependencies using Poetry
RUN poetry install --no-dev

# Copy the rest of the app code into the container
COPY . /app

# Expose port 8501 for Streamlit
EXPOSE 8501

# Run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "happiness-app.py", "--server.port=8501", "--server.address=0.0.0.0"]
