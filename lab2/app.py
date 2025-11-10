from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return f"Container is running. The secret key is: {os.environ.get('SECRET_KEY', 'NOT_SET')}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


