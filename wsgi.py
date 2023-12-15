# A webserver uses the file to enter the project.
# The init.py inside the app directory will be imported and run here.

from app import init_app

app = init_app()

@app.route('/api/login', methods=['OPTIONS'])
def handle_options():
    response = app.make_default_options_response()
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0")