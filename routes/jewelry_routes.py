"""Routes for Jewelry Planner with Multimodal Outfit Image Upload."""
import os
import uuid
from flask import request, jsonify, session
from werkzeug.utils import secure_filename
from PIL import Image

from config import Config
from routes import jewelry_bp
from services.gemini_client import GeminiPlannerService

def is_allowed_file(filename: str) -> bool:
    """Check if the uploaded file has an allowed image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@jewelry_bp.route("/generate-jewelry", methods=["POST"])
@jewelry_bp.route("/api/jewelry/generate", methods=["POST"])
def generate_jewelry_plan():
    """Endpoint for generating jewelry recommendations based on occasion, budget, and optional outfit image."""
    try:
        # Check whether request is multipart form or JSON
        if request.is_json:
            data = request.get_json(silent=True) or {}
            uploaded_file = None
        else:
            data = request.form.to_dict()
            uploaded_file = request.files.get("outfit_image")
            
        occasion = data.get("occasion", "Cocktail Party").strip()
        metal_preference = data.get("metal_preference", "Yellow Gold").strip()
        outfit_description = data.get("outfit_description", "").strip()
        
        try:
            budget = float(data.get("budget", 400.0))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Invalid budget value provided."}), 400
            
        if budget <= 0:
            return jsonify({"status": "error", "message": "Budget must be greater than zero."}), 400

        pil_image = None
        saved_image_url = None
        
        if uploaded_file and uploaded_file.filename and is_allowed_file(uploaded_file.filename):
            ext = uploaded_file.filename.rsplit(".", 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(uploaded_file.filename)}"
            save_path = Config.UPLOAD_FOLDER / unique_filename
            uploaded_file.save(save_path)
            saved_image_url = f"/static/uploads/{unique_filename}"
            
            try:
                with Image.open(save_path) as img:
                    pil_image = img.copy()
            except Exception as img_err:
                return jsonify({"status": "error", "message": f"Uploaded file is not a valid image: {img_err}"}), 400

        result = GeminiPlannerService.generate_jewelry_plan(
            occasion=occasion,
            budget=budget,
            metal_preference=metal_preference,
            outfit_description=outfit_description,
            outfit_image=pil_image
        )
        
        if saved_image_url:
            result["uploaded_outfit_url"] = saved_image_url

        session["last_jewelry_query"] = {
            "occasion": occasion,
            "budget": budget,
            "metal_preference": metal_preference
        }

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
