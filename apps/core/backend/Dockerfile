FROM python:3.7
# update pip and install pipenv
RUN pip install --upgrade pip && pip install pipenv
# environmen variables
ENV HOME=/home/backend \
    ENVIRONMENT=production \
    API_ENABLE_HTTPS_REDIRECT=False \
    API_ENABLE_CORS=True \
    API_SECRET=Iggl3Secret@ \
    API_MINUTES_EXPIRE_TOKEN=60 \
    CONNECTION_STRING=postgresql://postgres:postgres@localhost/postgres \
    CONNECTION_STRING_TEST=postgresql://postgres:postgres@localhost/testing
# define work directory
WORKDIR $HOME
# copy files to work directory
COPY . $HOME
# pipenv install dependencies
RUN pipenv install --deploy --ignore-pipfile
# configure expose port of application
EXPOSE 5000
# start application
CMD ["pipenv", "run", "python", "src/main.py"]