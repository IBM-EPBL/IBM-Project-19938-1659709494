from backend import create_app
import os

app = create_app()

port = os.environ.get("PORT", 5000)


if __name__ == '__main__':
    from waitress import serve
    serve(app, port=port)
