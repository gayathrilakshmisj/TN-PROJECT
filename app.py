"""Flask Application Entrypoint for AI Multi-Planner Suite.
Provides CORS, blueprint orchestration, session handling, and health endpoints.
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS

from config import Config
from routes import home_bp, party_bp, jewelry_bp

def create_app(config_class=Config):
    """Application factory for Flask app."""
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(config_class)

    # Enable CORS for cross-origin or frontend decoupled integrations
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Register modular blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(party_bp)
    app.register_blueprint(jewelry_bp)

    @app.route("/")
    def index():
        """Render the unified multi-planner interactive interface."""
        return render_template("index.html")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        """Check server status and AI configuration."""
        has_key = bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here")
        return jsonify({
            "status": "healthy",
            "service": "AI Multi-Planner API",
            "gemini_configured": has_key,
            "model": Config.GEMINI_MODEL,
            "fallback_enabled": Config.MOCK_FALLBACK_ON_ERROR
        }), 200

    return app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
    print(f" * AI Multi-Planner running on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
