import json
import os
from pathlib import Path

from flask import (jsonify, redirect, render_template, request,
                   send_from_directory, session, url_for)
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from . import ADMIN_PASSWORD_HASH, BASE_DIR, app, db
from .models import Event
from .utils import require_admin


@app.route("/")
def serve_index():
    return render_template("index.html")


@app.route("/contact")
def serve_contact():
    return render_template("contact.html")


@app.route("/pages/<path:path>")
def serve_pages(path):
    return send_from_directory(os.path.join(app.static_folder, "pages"), path)


@app.route("/assets/<path:path>")
def serve_assets(path):
    return send_from_directory(os.path.join(app.static_folder, "assets"), path)


@app.route("/api/events")
def get_events():
    # could database or other data source
    data_path = Path(__file__).parent / "data" / "events.json"
    with open("data/events.json") as f:
        events = json.load(f)
    return jsonify(events)


# TODO: implement sql_alchemy here
@app.route("/pages/contact", methods=["GET"])
def alumni_form():
    raise NotImplementedError("This function is not implemented.")


@app.route("/pages/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Handle form submission
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["msg"]

        # should this also be saved to db?
        subject = "New Contact Form Submission"
        body = f"""
                You have received a new message from your website contact form:

                Name: {name}
                Email: {email}
                Message:
                {message}
                """
        # _send_email(subject, body)

        # TODO: This info needs to be sent to designated email and saved to storage

        return redirect("/")  # Redirect to a thank you page or similar

    return redirect("/")


@app.route("/admin", methods=["GET"])
@require_admin
def admin():
    events = Event.query.all()
    return render_template("admin.html", events=events)


@app.route("/admin/add-event", methods=["POST"])
def add_event():
    upload_folder = os.path.join(BASE_DIR, "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = upload_folder

    # Get form fields
    title = request.form["title"]
    date = request.form["date"]
    description = request.form["description"]
    link = request.form["link"]
    file = request.files["image_file"]

    if file and file.filename:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        image_url = f"/static/uploads/{filename}"

    else:
        image_url = ""  # or set a default image path

    new_event = Event(
        title=title, date=date, description=description, image=image_url, link=link
    )
    db.session.add(new_event)
    db.session.commit()

    return redirect("/admin")


@app.route("/admin/delete-event", methods=["POST"])
def delete_event():
    event_id = request.form["id"]
    event = Event.Session.get(event_id)
    if event:
        if event.image and event.image.startswith("/static/uploads/"):
            # Build the full path from the relative URL
            image_path = os.path.join(BASE_DIR, event.image.lstrip("/"))
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except Exception as e:
                    print(f"Warning: Could not delete image file: {e}")

        db.session.delete(event)
        db.session.commit()
    return redirect("/admin")


@app.route("/events", methods=["GET"])
def event():
    events = Event.query.all()
    return render_template("events.html", events=events)


@app.get("/admin/login")
def admin_login():
    # If already logged in, go to target
    nxt = request.args.get("next") or url_for("admin_panel")
    if session.get("is_admin"):
        return redirect(nxt)
    return render_template("admin_login.html", next=nxt)


@app.post("/admin/login")
def admin_login_post():
    password = request.form.get("password", "")
    nxt = request.form.get("next") or url_for("admin_panel")
    if check_password_hash(ADMIN_PASSWORD_HASH, password):
        session["is_admin"] = True
        session.permanent = False
        return redirect(nxt)
    return render_template("admin_login.html", next=nxt, error="Invalid password.")


@app.post("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))
