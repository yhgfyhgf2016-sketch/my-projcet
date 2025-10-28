from flask import Blueprint, request, jsonify, send_file
import os
import sys
import tempfile
from datetime import datetime

# Add the parent directory to the path to import generate_pdf and verify_qr
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import db from database module
from database import db
from src.models.certificate import Certificate

certificate_bp = Blueprint('certificate', __name__)

@certificate_bp.route('/certificates', methods=['POST'])
def create_certificate():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'id_number', 'issue_date', 'expiry_date']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if certificate with this ID already exists
        existing_cert = Certificate.query.filter_by(id_number=data['id_number']).first()
        if existing_cert:
            return jsonify({'error': 'Certificate with this ID number already exists'}), 400
        
        # Generate certificate number
        cert_count = Certificate.query.count()
        certificate_number = f"HC{cert_count + 1:06d}"
        
        # Create QR code data
        qr_data = f"Name: {data['name']}\nID: {data['id_number']}\nCertificate: {certificate_number}\nIssue Date: {data['issue_date']}\nExpiry Date: {data['expiry_date']}"
        
        # Create new certificate
        certificate = Certificate(
            name=data['name'],
            id_number=data['id_number'],
            nationality=data.get('nationality', 'سعودي'),
            profession=data.get('profession', 'عامل'),
            issue_date=data['issue_date'],
            expiry_date=data['expiry_date'],
            certificate_number=certificate_number,
            program_type=data.get('program_type', 'برنامج تثقيفي صحي'),
            program_expiry=data.get('program_expiry', data['expiry_date']),
            qr_code_data=qr_data
        )
        
        db.session.add(certificate)
        db.session.commit()
        
        return jsonify({
            'message': 'Certificate created successfully',
            'certificate': certificate.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificate_bp.route('/certificates/<id_number>/verify', methods=['GET'])
def verify_certificate(id_number):
    try:
        certificate = Certificate.query.filter_by(id_number=id_number).first()
        if not certificate:
            return jsonify({'error': 'Certificate not found', 'valid': False}), 404
        
        return jsonify({
            'valid': True,
            'certificate': certificate.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificate_bp.route('/certificates/<id_number>/pdf', methods=['GET'])
def generate_certificate_pdf(id_number):
    try:
        certificate = Certificate.query.filter_by(id_number=id_number).first()
        if not certificate:
            return jsonify({'error': 'Certificate not found'}), 404
        
        # Import the generate_pdf function
        from generate_pdf import create_certificate_pdf
        
        certificate_data = {
            'name': certificate.name,
            'id_number': certificate.id_number,
            'nationality': certificate.nationality,
            'profession': certificate.profession,
            'issue_date': certificate.issue_date,
            'expiry_date': certificate.expiry_date,
            'certificate_number': certificate.certificate_number,
            'program_type': certificate.program_type,
            'program_expiry': certificate.program_expiry
        }
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_path = tmp_file.name
        
        create_certificate_pdf(pdf_path, certificate_data)
        
        return send_file(pdf_path, as_attachment=True, download_name=f"certificate_{id_number}.pdf")
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificate_bp.route('/verify-qr', methods=['POST'])
def verify_qr_code():
    try:
        if 'pdf_file' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        pdf_file = request.files['pdf_file']
        if pdf_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdf_file.save(tmp_file.name)
            temp_path = tmp_file.name
        
        # Import the verify_qr function
        from verify_qr import verify_qr_code
        
        qr_data = verify_qr_code(temp_path)
        
        # Clean up the temporary file
        os.remove(temp_path)
        
        if qr_data:
            # Try to find a matching certificate in the database
            # Extract ID from QR data (assuming format "Name: ...\nID: ...\n...")
            lines = qr_data.split('\n')
            id_number = None
            for line in lines:
                if line.startswith('ID: '):
                    id_number = line.replace('ID: ', '').strip()
                    break
            
            if id_number:
                certificate = Certificate.query.filter_by(id_number=id_number).first()
                if certificate:
                    return jsonify({
                        'valid': True,
                        'qr_data': qr_data,
                        'certificate': certificate.to_dict()
                    }), 200
                else:
                    return jsonify({
                        'valid': False,
                        'qr_data': qr_data,
                        'message': 'Certificate not found in database'
                    }), 404
            else:
                return jsonify({
                    'valid': False,
                    'qr_data': qr_data,
                    'message': 'Invalid QR code format'
                }), 400
        else:
            return jsonify({
                'valid': False,
                'message': 'No QR code found in the PDF'
            }), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@certificate_bp.route('/certificates', methods=['GET'])
def list_certificates():
    try:
        certificates = Certificate.query.all()
        return jsonify({
            'certificates': [cert.to_dict() for cert in certificates]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

