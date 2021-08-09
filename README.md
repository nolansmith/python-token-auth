# POTS Back End

### Cloning the Repo
```
git clone git@github.com:nolansmith/python-token-auth.git
cd python-token-auth
```
## Initial Setup (all commands in project root directory)
### Setting up python virtual environment
```
python -m venv env
```

### Activating virtual environment (linux/bash)
```
source ./env/Scripts/activate
```

### Activating virtual environment (windows)
```
"env\Scripts\activate.bat"
```

### Install pipenv and packages
```
pip install pipenv
pipenv install
```


## Setting up Docker Container (for Postgres)
```
docker-compose up -d
```

## Create a `.env` file locally
```
POSTGRES_CONN_STRING="postgresql://dev:dev@localhost:5432/potsdevdb"
```
## Migrations (proper database models)
```
flask db upgrade
```

## Seeding (only when setting up)
```
flask seed-db
```

## Run App
```
flask run
```

# After Initial Setup
## Migrations
Using the code-first approach with SQL Alchemy ORM, model changes are made via code in the ``` models ``` folder
After changes are made, execute
``` 
flask db migrate
flask db upgrade 
```

## Accessing postgres to check things
Execute ``` psql -h localhost -p 5432 -d potsdevdb -U dev ``` in your terminal and enter `dev` as the password. 

## Running the app and container after initial setup
Once you start docker, run `docker ps` to make sure the postgres container is running. If not, you can execute `docker-compose up -d` in the project's root directory. Running the flask app is a simple `flask run`

## Virtual environment and installing packages
Be sure to activate the virtual environment with one of the activation commands further up on the page. `(env)` Should precede your terminal. Instead of using `pip` use `pipenv` for installing packages as they'll go to that environment's Pipfile.

