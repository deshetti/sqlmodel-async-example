# SQLModel Aysnc Example

This is a simple repo I created with a working example to demonstrate async tools usage with SQLModel. Purpose was to add this to the SQLModel documentation.

If you want to run this project directly, you can follow the below steps:

- Run the docker-compose.yaml file to start the Postgres instance and create the required database
- Run the fastapi application in a different terminal using the command: `poetry run python main.py`
- You should be able to access the swagger docs for the fastapi application at https://localhost:8000/docs