import logging
from pathlib import Path
from flask import Blueprint, request, jsonify, url_for
from config import Config
from model.utils import is_allowed_file, generate_unique_filename
from services.classifier import run_classification_pipeline, get_model
from services.report_generator import generate_pdf_report
from services.database import get_history, get_prediction_by_id, delete_prediction, get_dashboard_stats

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint indicating model readiness and service health."""
    model = get_model()
    model_status = "loaded" if model is not None else "fallback_mode"
    return jsonify({
        'status': 'healthy',
        'model_status': model_status,
        'app_name': 'HematoVision AI Medical Server',
        'version': '2.0.0'
    }), 200

@api_bp.route('/predict', methods=['POST'])
def api_predict():
    """
    REST API endpoint for blood cell image classification.
    Expects multipart/form-data upload with key 'file'.
    """
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Missing file payload in request'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
        
    if not is_allowed_file(file.filename):
        return jsonify({
            'status': 'error', 
            'message': f"Unsupported file format. Allowed: {list(Config.ALLOWED_EXTENSIONS)}"
        }), 400
        
    try:
        unique_name = generate_unique_filename(file.filename)
        saved_path = Config.UPLOAD_FOLDER / unique_name
        file.save(str(saved_path))
        
        result = run_classification_pipeline(saved_path, file.filename)
        report_path = generate_pdf_report(result)
        result['report_url'] = f"/reports/{Path(report_path).name}"
        
        return jsonify({
            'status': 'success',
            'data': result
        }), 200
        
    except Exception as e:
        logger.error(f"API prediction error: {e}", exc_info=True)
        return jsonify({'status': 'error', 'message': str(e)}), 500

@api_bp.route('/history', methods=['GET'])
def api_history():
    """Fetch prediction history with optional search, class filter, limit, and offset."""
    search = request.args.get('search')
    filter_class = request.args.get('class')
    limit = int(request.args.get('limit', 50))
    offset = int(request.args.get('offset', 0))
    
    records = get_history(search=search, filter_class=filter_class, limit=limit, offset=offset)
    return jsonify({
        'status': 'success',
        'count': len(records),
        'data': records
    }), 200

@api_bp.route('/history/<int:pred_id>', methods=['GET'])
def api_get_single_history(pred_id):
    """Retrieve details for a single prediction by ID."""
    record = get_prediction_by_id(pred_id)
    if not record:
        return jsonify({'status': 'error', 'message': 'Prediction record not found'}), 404
        
    return jsonify({
        'status': 'success',
        'data': record
    }), 200

@api_bp.route('/history/<int:pred_id>', methods=['DELETE'])
def api_delete_history(pred_id):
    """Delete a prediction record and clean up associated files."""
    success = delete_prediction(pred_id)
    if not success:
        return jsonify({'status': 'error', 'message': 'Record not found or could not be deleted'}), 404
        
    return jsonify({
        'status': 'success',
        'message': f"Prediction ID {pred_id} deleted successfully."
    }), 200

@api_bp.route('/statistics', methods=['GET'])
def api_statistics():
    """Retrieve aggregate clinical dashboard statistics."""
    stats = get_dashboard_stats()
    return jsonify({
        'status': 'success',
        'data': stats
    }), 200
