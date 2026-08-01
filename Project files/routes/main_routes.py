import logging
from flask import Blueprint, render_template, request, send_from_directory, abort
from config import Config
from services.database import get_history, get_prediction_by_id, get_dashboard_stats

logger = logging.getLogger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render main upload page."""
    return render_template('index.html', classes=Config.CLASS_NAMES)

@main_bp.route('/about')
def about():
    """Render educational about page."""
    return render_template('about.html', cell_info=Config.CELL_INFO)

@main_bp.route('/dashboard')
def dashboard():
    """Render analytics dashboard page."""
    stats = get_dashboard_stats()
    return render_template('dashboard.html', stats=stats)

@main_bp.route('/history')
def history():
    """Render searchable prediction history page."""
    search = request.args.get('search', '').strip()
    filter_class = request.args.get('class', '').strip()
    records = get_history(search=search, filter_class=filter_class)
    return render_template('history.html', records=records, search=search, filter_class=filter_class, classes=Config.CLASS_NAMES)

@main_bp.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded specimen and Grad-CAM images."""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@main_bp.route('/reports/<path:filename>')
def serve_report(filename):
    """Serve generated diagnostic PDF reports."""
    return send_from_directory(Config.REPORT_FOLDER, filename, as_attachment=True)
