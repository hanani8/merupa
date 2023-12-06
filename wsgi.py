# A webserver uses the file to enter the project.
# The init.py inside the app directory will be imported and run here.

from app import init_app

app = init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
