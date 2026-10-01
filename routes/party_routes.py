"""Routes for Party Planner."""
from flask import request, jsonify, session
from routes import party_bp
from services.gemini_client import GeminiPlannerService

@party_bp.route("/generate-party", methods=["POST"])
@party_bp.route("/api/party/generate", methods=["POST"])
def generate_party_plan():
    """Endpoint for generating event timeline, catering, decor, and budget allocation."""
    try:
        data = request.get_json(silent=True) or request.form.to_dict()
        
        event_type = data.get("event_type", "Birthday Celebration").strip()
        theme = data.get("theme", "Modern Chic").strip()
        dietary_notes = data.get("dietary_notes", "").strip()
        
        try:
            guest_count = int(data.get("guest_count", 20))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Guest count must be an integer."}), 400
            
        try:
            budget = float(data.get("budget", 600.0))
        except (ValueError, TypeError):
            return jsonify({"status": "error", "message": "Invalid budget value provided."}), 400
            
        if guest_count <= 0:
            return jsonify({"status": "error", "message": "Guest count must be at least 1."}), 400
            
        if budget <= 0:
            return jsonify({"status": "error", "message": "Budget must be greater than zero."}), 400

        result = GeminiPlannerService.generate_party_plan(
            event_type=event_type,
            guest_count=guest_count,
            budget=budget,
            theme=theme,
            dietary_notes=dietary_notes
        )
        
        session["last_party_query"] = {
            "event_type": event_type,
            "guest_count": guest_count,
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
