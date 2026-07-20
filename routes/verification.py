from flask import Blueprint, jsonify, render_template, request

from services.upload.upload_service import UploadService

verification_bp = Blueprint("verification", __name__)
upload_service = UploadService()


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
