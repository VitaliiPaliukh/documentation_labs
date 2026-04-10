"""Run script for Lab 3 MVC web app."""
from web.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

