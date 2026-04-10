"""Flask MVC application for Lab 3."""
from flask import Flask, g, redirect, render_template, url_for

from config import DATABASE_URL
from main import DependencyContainer
from web.controllers.patient_controller import patients_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "lab3-secret-key"

    app.register_blueprint(patients_bp)

    @app.before_request
    def _build_request_container():
        # Request-scoped DI container keeps session lifecycle explicit.
        g.container = DependencyContainer(DATABASE_URL)

    @app.teardown_request
    def _cleanup_request_container(exception):
        container = getattr(g, "container", None)
        if container is not None:
            container.cleanup()

    @app.route("/")
    def home():
        return redirect(url_for("patients.list_patients"))

    @app.route("/appointments")
    def list_appointments():
        appointments = g.container.appointment_management_service.get_all_appointments()
        return render_template("appointments/list.html", appointments=appointments)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)

