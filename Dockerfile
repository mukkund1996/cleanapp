# Use the official lightweight Python image.
FROM python:3.6-slim-buster

# Copy the contents into the docker container and set the work dir
ENV APP_HOME=/CleanApp
WORKDIR $APP_HOME
COPY . ./

# Setting up the environment variable for the Google API secret file
ENV CREDENTIALS_JSON=/CleanApp/credentials.json
RUN pip install .

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 cleanapp.app:server