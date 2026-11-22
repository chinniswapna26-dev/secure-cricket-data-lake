
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import csv
import os
import shutil
import uuid
import pyotp
import qrcode

from werkzeug.utils import secure_filename
from database import (
    init_db, create_user, get_user, verify_password,
    save_mfa_secret, count_users, get_all_users,
    update_user_role
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is required")

UPLOAD_FOLDER = "data/raw-data"
REPORTS_FOLDER = "data/reports"
QR_FOLDER = os.path.join("static", "qr_codes")

ALLOWED_EXTENSIONS = {"csv"}
MAX_FILE_SIZE = 5 * 1024 * 1024

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)

init_db()


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or len(username) < 3:
            flash("Username must contain at least 3 characters.")
            return render_template("register.html")

        if len(username) > 30:
            flash("Username cannot exceed 30 characters.")
            return render_template("register.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.")
            return render_template("register.html")
        role = "Read-only User"
        if not create_user(username, password, role):
            flash("Username already exists.")
            return render_template("register.html")

        secret = pyotp.random_base32()
        save_mfa_secret(username, secret)

        user = get_user(username)
        session.clear()
        session["username"] = username
        session["role"] = user["role"]

        otp_uri = pyotp.TOTP(secret).provisioning_uri(
            name=username,
            issuer_name="Secure Cricket Data Lake"
        )

        qr_filename = str(uuid.uuid4()) + ".png"
        qr_path = os.path.join(QR_FOLDER, qr_filename)

        qrcode.make(otp_uri).save(qr_path)

        session["mfa_setup"] = True

        return render_template(
            "setup_mfa.html",
            qr_file="qr_codes/" + qr_filename
        )

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        mfa_code = request.form.get("mfa_code", "").strip()

        user = get_user(username)
        if user and verify_password(user, password):
            if not user["mfa_secret"]:
                flash("MFA setup is required. Please contact the administrator.")
                return render_template("login.html")

            if pyotp.TOTP(user["mfa_secret"]).verify(
                mfa_code, valid_window=1
            ):
                admin_username = os.environ.get("ADMIN_USERNAME", "").strip()

                if admin_username and username == admin_username:
                    updated = update_user_role(user["id"], "Administrator")
                    user = get_user(username)
                    app.logger.info(
                        "Admin promotion: updated=%s, role=%s",
                        updated, user["role"] if user else "USER NOT FOUND"
                    )
                session.clear()
                session["username"] = username
                session["role"] = user["role"]
                return redirect(url_for("dashboard"))

        flash("Invalid username, password or MFA code.")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"]
    )


@app.route("/admin")
def admin():
    if session.get("role") != "Administrator":
        return "Access denied: Administrator only.", 403

    users = [dict(user) for user in get_all_users()]

    return render_template("admin.html", users=users)


@app.route("/admin/update-role", methods=["POST"])
def admin_update_role():
    if session.get("role") != "Administrator":
        return "Access denied: Administrator only.", 403

    try:
        user_id = int(request.form.get("user_id", ""))
    except ValueError:
        return "Invalid user ID.", 400

    role = request.form.get("role", "")

    if role not in ["Data Analyst", "Coach", "Read-only User"]:
        return "Invalid role.", 400

    users = get_all_users()
    target = next(
        (user for user in users if user["id"] == user_id),
        None
    )

    if target is None:
        return "User not found.", 404

    if target["role"] == "Administrator":
        return "Administrator role cannot be changed here.", 403

    update_user_role(user_id, role)
    flash("User role updated successfully.")

    return redirect(url_for("admin"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "username" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Data Analyst":
        return "Access denied: only Data Analysts can upload datasets.", 403

    if request.method == "POST":
        match_name = request.form.get("match_name", "").strip()
        category = request.form.get("category", "").strip()
        file = request.files.get("file")

        if not match_name or not category or not file:
            return "Please provide all required details."

        if file.filename == "":
            return "Please select a CSV file."

        if not allowed_file(file.filename):
            return "Only CSV files are allowed."

        safe_name = secure_filename(file.filename)

        if not safe_name:
            return "Invalid filename."

        unique_name = str(uuid.uuid4()) + "_" + safe_name
        save_path = os.path.join(
            app.config["UPLOAD_FOLDER"], unique_name
        )

        file.save(save_path)

        return """
        <h2>Dataset Uploaded Successfully!</h2>
        <p>Match: {}</p>
        <p>Category: {}</p>
        <p>File: {}</p>
        <a href="/dashboard">Back to Dashboard</a>
        """.format(match_name, category, safe_name)

    return render_template("upload.html")


@app.route("/reports")
def reports():
    if "username" not in session:
        return redirect(url_for("login"))

    upload_path = app.config["UPLOAD_FOLDER"]

    csv_files = [
        os.path.join(upload_path, name)
        for name in os.listdir(upload_path)
        if allowed_file(name)
    ]

    players = []

    if csv_files:
        latest_file = max(csv_files, key=os.path.getmtime)

        with open(
            latest_file,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as csvfile:
            reader = csv.DictReader(csvfile)
            players = list(reader)

    return render_template("reports.html", players=players)


@app.route("/download-report")
def download_report():
    if "username" not in session:
        return redirect(url_for("login"))

    upload_path = app.config["UPLOAD_FOLDER"]

    csv_files = [
        os.path.join(upload_path, name)
        for name in os.listdir(upload_path)
        if allowed_file(name)
    ]

    if not csv_files:
        return "No report available to download."

    latest_file = max(csv_files, key=os.path.getmtime)

    os.makedirs(REPORTS_FOLDER, exist_ok=True)

    report_path = os.path.join(
        REPORTS_FOLDER, "cricket_report.csv"
    )

    shutil.copy2(latest_file, report_path)

    return send_file(
        report_path,
        as_attachment=True,
        download_name="cricket_report.csv",
        mimetype="text/csv"
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

