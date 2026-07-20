from dataclasses import asdict

from flask import Blueprint, jsonify, render_template, request

from services.upload.upload_service import UploadService
from services.verification.verification_service import VerificationService

verification_bp = Blueprint("verification", __name__)
upload_service = UploadService()
verification_service = VerificationService()


@verification_bp.route("/verification")
def verification():
    return render_template("verification.html")


@verification_bp.route("/api/upload/id", methods=["POST"])
def upload_id():

    uploaded_file = request.files.get("file")

    if uploaded_file is None:
        return (
            jsonify(
                {
                    "success": False,
                    "message": "No files uploaded",
                }
            ),
            400,
        )

    saved_path = upload_service.save_file(uploaded_file, "ids")

    return jsonify({"success": True, "path": saved_path}), 200


@verification_bp.route("/api/upload/live", methods=["POST"])
def upload_live_face():

    uploaded_file = request.files.get("file")

    if uploaded_file is None:
        return jsonify({"sucess": False, "message": "No file Uploaded"}), 400

    saved_path = upload_service.save_file(uploaded_file, "live")

    return jsonify({"success": True, "path": saved_path}), 200


@verification_bp.route("/api/verify", methods=["POST"])
def verify():

    data = request.get_json()

    result = verification_service.verify_user(
        id_image_path=data["id_image_path"],
        live_image_path=data["live_image_path"],
        id_type=data["id_type"],
        liveness_passed=data["liveness_passed"],
    )

    return jsonify(asdict(result)), 200
