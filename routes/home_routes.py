"""Routes for Home Interior Planner."""
from flask import request, jsonify, session
from routes import home_bp
from services.gemini_client import GeminiPlannerService

@home_bp.route("/generate-home", methods=["POST"])
@home_bp.route("/api/home/generate", methods=["POST"])
def generate_home_plan():
    """Endpoint for generating an interior room plan and shopping list."""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        
        room_type = data.get("room_type", "Living Room").strip()
        style = data.get("style", "Modern Minimalist").strip()
        dimensions = data.get("dimensions", "").strip()
        extra_notes = data.get("extra_notes", "").strip()
        
        try:
            budget = float(data.get("budget", 1500.0))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Invalid budget value provided."}), 400
            
        if budget <= 0:
            return jsonify({"status": "error", "message": "Budget must be greater than zero."}), 400

        result = GeminiPlannerService.generate_home_plan(
            room_type=room_type,
            style=style,
            budget=budget,
            dimensions=dimensions,
            extra_notes=extra_notes
        )
        
        # Save search criteria to session for user history
        session["last_home_query"] = {
            "room_type": room_type,
            "style": style,
            "budget": budget
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
