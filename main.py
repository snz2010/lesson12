from app import app
from settings import CONFIG


if __name__ == '__main__':
    app.config.update(CONFIG)
    app.run(debug=app.config['DEBUG'])
