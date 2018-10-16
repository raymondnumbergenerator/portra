from flask import Flask

app = Flask(__name__)
app.config.from_envvar('PORTRA_SETTINGS')

import portra.views

if __name__ == '__main__':
    exit(app.run(debug=True))
