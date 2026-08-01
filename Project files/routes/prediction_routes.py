import os
import logging
from pathlib import Path
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify, send_file
from config import Config
from model.utils import is_allowed_file, generate_unique_filename
from services.classifier import run_classification_pipeline
from services.report_generator import generate_pdf_report
from services.database import get_prediction_by_id

logger = logging.getLogger(__name__)

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/upload-predict', methods=['POST'])
def upload_predict():
    """
    Form submission handler for image upload and inference.
    """
    if 'file' not in request.files:
        flash('No file provided in the upload request.', 'danger')
        return redirect(url_for('main.index'))
        
    file = request.files['file']
    if file.filename == '':
        flash('No file selected for classification.', 'warning')
        return redirect(url_for('main.index'))
        
    if not is_allowed_file(file.filename):
        flash(f"Invalid file type. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}", 'danger')
        return redirect(url_for('main.index'))
        
    try:
        unique_name = generate_unique_filename(file.filename)
        saved_path = Config.UPLOAD_FOLDER / unique_name
        file.save(str(saved_path))
        
        result = run_classification_pipeline(saved_path, file.filename)
        
        # Auto-generate PDF report
        report_path = generate_pdf_report(result)
        result['report_url'] = f"/reports/{Path(report_path).name}"
        
        return render_template('result.html', result=result)
        
    except Exception as e:
        logger.error(f"Prediction pipeline failure: {e}", exc_info=True)
        flash(f"Error processing image specimen: {str(e)}", 'danger')
        return redirect(url_for('main.index'))

@prediction_bp.route('/download-report/<int:pred_id>')
def download_report(pred_id):
    """Generate or serve existing PDF report for a prediction ID."""
    record = get_prediction_by_id(pred_id)
    if not record:
        flash('Prediction record not found.', 'danger')
        return redirect(url_for('main.history'))
        
    report_path = record.get('report_path')
    if not report_path or not Path(report_path).exists():
        # Regenerate report
        report_path = generate_pdf_report(record)
        
    return send_file(report_path, as_attachment=True, download_name=f"HematoVision_Report_{pred_id}.pdf")
