import logging
from pathlib import Path
from flask import Flask, render_template, jsonify
from config import Config
from services.database import init_db
from routes.main_routes import main_bp
from routes.prediction_routes import prediction_bp
from routes.api_routes import api_bp

# Ensure runtime directories exist
Config.init_app()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Config.LOG_FOLDER / 'app.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

def create_app() -> Flask:
    """Flask Application Factory."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize runtime folders and database
    Config.init_app()
    init_db()
    
    # Register Blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(prediction_bp)
    app.register_blueprint(api_bp)
    
    # Error Handlers
    @app.errorhandler(404)
    def not_found_error(error):
        if request_is_json():
            return jsonify({'status': 'error', 'message': 'Resource not found'}), 404
        return render_template('base.html', page_title="Page Not Found"), 404

    @app.errorhandler(413)
    def file_too_large_error(error):
        return jsonify({'status': 'error', 'message': 'File size exceeds maximum 16MB limit.'}), 413

    @app.errorhandler(500)
    def internal_server_error(error):
        logger.error(f"Internal Server Error: {error}", exc_info=True)
        if request_is_json():
            return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500
        return render_template('base.html', page_title="Server Error"), 500

    def request_is_json():
        from flask import request
        return request.path.startswith('/api/') or request.headers.get('Accept') == 'application/json'

    logger.info("HematoVision Application initialized successfully.")
    return app

app = create_app()

if __name__ == '__main__':
    logger.info("Starting HematoVision Web Application on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
