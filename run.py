from portra.app import app

import portra.views

if __name__ == '__main__':
    exit(app.run(host='0.0.0.0', port=8513, debug=True))
