import os
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from config import Config
from services.database import update_report_path

logger = logging.getLogger(__name__)

def generate_pdf_report(pred_data: Dict[str, Any]) -> str:
    """
    Generate a hospital-grade diagnostic PDF report for a prediction result.
    """
    Config.init_app()
    report_filename = f"report_pred_{pred_data['id']}.pdf"
    report_filepath = Config.REPORT_FOLDER / report_filename

    doc = SimpleDocTemplate(
        str(report_filepath),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=0
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b')
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    
    bold_body = ParagraphStyle(
        'BoldBody',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    story = []
    
    # Header Section
    header_data = [
        [
            Paragraph("<b>HEMATOVISION CLINICAL DIAGNOSTICS</b><br/><font color='#64748b' size=9>AI-Powered Automated Hematology Analysis</font>", title_style),
            Paragraph(f"<b>Report ID:</b> HV-{pred_data['id']:06d}<br/><b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", subtitle_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[4.2*inch, 3.2*inch])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT')
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=15))
    
    # Specimen & Diagnosis Summary Card
    pred_class = pred_data['predicted_class']
    confidence = pred_data['confidence']
    inf_time = pred_data['inference_time']
    orig_file = pred_data.get('original_filename', 'Unknown')
    
    summary_text = f"""
    <b>Primary Classification:</b> <font color='#0284c7' size=12><b>{pred_class.upper()}</b></font><br/>
    <b>Prediction Confidence:</b> <b>{confidence}%</b><br/>
    <b>Inference Latency:</b> {inf_time} ms<br/>
    <b>Original Specimen:</b> {orig_file}
    """
    
    cell_info = Config.CELL_INFO.get(pred_class, {})
    description_text = cell_info.get('description', '')
    range_text = cell_info.get('normal_range', '')
    
    clinical_notes = f"""
    <b>Normal Reference Range:</b> {range_text}<br/>
    <b>Clinical Description:</b> {description_text}
    """
    
    card_data = [
        [Paragraph(summary_text, body_style), Paragraph(clinical_notes, body_style)]
    ]
    card_table = Table(card_data, colWidths=[3.7*inch, 3.7*inch])
    card_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP')
    ]))
    story.append(card_table)
    story.append(Spacer(1, 15))
    
    # Visual Image Comparison Section
    story.append(Paragraph("Microscopic Specimen & Explainable AI (Grad-CAM)", section_heading))
    
    orig_img_path = Config.UPLOAD_FOLDER / pred_data['filename']
    gradcam_img_path = Config.UPLOAD_FOLDER / f"gradcam_{pred_data['filename']}"
    
    img_cells = []
    if orig_img_path.exists():
        img_cells.append(RLImage(str(orig_img_path), width=3.3*inch, height=2.4*inch))
    else:
        img_cells.append(Paragraph("Original Specimen Image Unavailable", body_style))
        
    if gradcam_img_path.exists():
        img_cells.append(RLImage(str(gradcam_img_path), width=3.3*inch, height=2.4*inch))
    else:
        img_cells.append(Paragraph("Grad-CAM Heatmap Image Unavailable", body_style))
        
    img_table_data = [
        img_cells,
        [Paragraph("<b>Original Microscopic View</b>", bold_body), Paragraph("<b>Grad-CAM Salience Heatmap</b>", bold_body)]
    ]
    img_table = Table(img_table_data, colWidths=[3.7*inch, 3.7*inch])
    img_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,1), (-1,1), 10)
    ]))
    story.append(img_table)
    story.append(Spacer(1, 15))
    
    # Probability Distribution Table
    story.append(Paragraph("Full Probability Distribution", section_heading))
    top_probs = pred_data.get('top_probabilities', {})
    
    prob_table_data = [
        [Paragraph("<b>Blood Cell Type</b>", bold_body), Paragraph("<b>Classification Probability (%)</b>", bold_body), Paragraph("<b>Relative Score</b>", bold_body)]
    ]
    for cell_type, prob in top_probs.items():
        is_winner = (cell_type == pred_class)
        cell_label = f"<b>{cell_type}</b> (Primary)" if is_winner else cell_type
        bar_visual = "█" * int(prob / 5)
        prob_table_data.append([
            Paragraph(cell_label, body_style),
            Paragraph(f"{prob:.2f}%", body_style),
            Paragraph(f"<font color='#0284c7'>{bar_visual}</font>", body_style)
        ])
        
    prob_table = Table(prob_table_data, colWidths=[2.5*inch, 2.5*inch, 2.4*inch])
    prob_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    story.append(prob_table)
    story.append(Spacer(1, 20))
    
    # Medical Disclaimer Footer
    disclaimer_text = """
    <b>CLINICAL DISCLAIMER:</b> HematoVision is an auxiliary decision-support tool powered by deep transfer learning (MobileNetV2). 
    This report is generated automatically for educational and preliminary clinical screening purposes. 
    It does NOT constitute a final medical diagnosis. All findings must be reviewed and verified by a licensed Hematologist or Clinical Pathologist.
    """
    disclaimer_table = Table([[Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=body_style, fontSize=8, leading=11, textColor=colors.HexColor('#475569')))]], colWidths=[7.4*inch])
    disclaimer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f1f5f9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('PADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(disclaimer_table)
    
    doc.build(story)
    logger.info(f"Generated diagnostic PDF report at {report_filepath}")
    
    # Update DB record
    update_report_path(pred_data['id'], str(report_filepath))
    
    return str(report_filepath)
