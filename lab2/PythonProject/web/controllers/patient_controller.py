"""Patient MVC controller."""
from flask import Blueprint, render_template, request, redirect, url_for, flash

patients_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patients_bp.route("/")
def list_patients():
    container = _get_container()
    patients = container.patient_management_service.get_all_patients()
    return render_template("patients/list.html", patients=patients)


@patients_bp.route("/<int:patient_id>")
def patient_details(patient_id: int):
    container = _get_container()
    patient = container.patient_management_service.get_patient_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for("patients.list_patients"))
    return render_template("patients/details.html", patient=patient)


@patients_bp.route("/create", methods=["GET", "POST"])
def create_patient():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        insurance_number = request.form.get("insurance_number", "").strip()

        if not full_name or not phone:
            flash("Full name and phone are required.", "error")
            return render_template("patients/form.html", title="Create Patient", patient=None)

        container = _get_container()
        container.patient_management_service.create_patient(full_name, phone, insurance_number)
        flash("Patient created successfully.", "success")
        return redirect(url_for("patients.list_patients"))

    return render_template("patients/form.html", title="Create Patient", patient=None)


@patients_bp.route("/<int:patient_id>/edit", methods=["GET", "POST"])
def edit_patient(patient_id: int):
    container = _get_container()
    patient = container.patient_management_service.get_patient_by_id(patient_id)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for("patients.list_patients"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        insurance_number = request.form.get("insurance_number", "").strip()

        if not full_name or not phone:
            flash("Full name and phone are required.", "error")
            return render_template("patients/form.html", title="Edit Patient", patient=patient)

        try:
            container.patient_management_service.update_patient(
                patient_id=patient_id,
                full_name=full_name,
                phone=phone,
                insurance_number=insurance_number,
            )
            flash("Patient updated successfully.", "success")
            return redirect(url_for("patients.patient_details", patient_id=patient_id))
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("patients.list_patients"))
        except Exception as exc:
            flash(f"Could not update patient: {exc}", "error")
            return redirect(url_for("patients.list_patients"))

    return render_template("patients/form.html", title="Edit Patient", patient=patient)


@patients_bp.route("/<int:patient_id>/delete", methods=["POST"])
def delete_patient(patient_id: int):
    container = _get_container()
    try:
        container.patient_management_service.delete_patient(patient_id)
        flash("Patient deleted successfully.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    except Exception as exc:
        flash(f"Could not delete patient: {exc}", "error")
    return redirect(url_for("patients.list_patients"))


def _get_container():
    """Resolve request-scoped dependency container from Flask app context."""
    from flask import g

    return g.container

