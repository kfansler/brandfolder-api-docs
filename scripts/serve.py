# serve.py

from flask import Flask
from flask import send_from_directory

# creates a Flask application, named app
app = Flask(__name__)

@app.route("/")
def openapi():
    return send_from_directory('/openapi/generated/spec','index.html')

@app.route('/<filename>')
def spec(filename):
    return send_from_directory('/openapi/generated/spec', filename)

@app.route('/images/<filename>')
def image(filename):
    return send_from_directory('/openapi/generated/spec/images', filename)

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    response.cache_control.no_cache = True
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    response.cache_control.proxy_revalidate = True
    return response

# run the application
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
