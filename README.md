# World Happiness Report (2015-2019) Visualisation

Author: Elise Barattini

This project uses data from the World Happiness Report to demonstrate how to build a Streamlit app and run it locally or as a Docker container.

## Data
The dataset used is world_happiness_combined.csv, which consists of five public [Kaggle datasets](https://www.kaggle.com/datasets/unsdsn/world-happiness) (one for each year of the report) merged together. retrieved from which contains global happiness data. The dataset has been included in the data/ folder of this repository. Ensure the dataset is present in this folder before running the app.

## Running the app locally
### 1. Create a virtual environment
If you are not using Poetry, you can create a virtual environment manually:

```setup
python3 -m venv .venv
source .venv/bin/activate
```
### 2. Install requirements
Install dependencies using Poetry (this project uses Poetry for dependency management):

```setup
poetry install
```
### 3. Run the app
Once the environment is set up, run the app locally:
```setup
poetry run streamlit run happiness-app.py
```

## Running the app on Docker
### 1. Build the Docker image
Build the Docker image using the provided Dockerfile:
```setup
docker build -t streamlit-happiness-app .
```

### 2. Run the Docker container
Run the app within a Docker container:
```setup
docker run -p 8501:8501 streamlit-happiness-app
```

After running the command, open your browser and go to http://localhost:8501 to view the app.





