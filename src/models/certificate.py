from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Import db from database module
from database import db

class Certificate(db.Model):
    __tablename__ = 'certificates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    id_number = db.Column(db.String(50), nullable=False, unique=True)
    nationality = db.Column(db.String(50), nullable=False, default="سعودي")
    profession = db.Column(db.String(100), nullable=False, default="عامل")
    issue_date = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.String(50), nullable=False)
    certificate_number = db.Column(db.String(50), nullable=False)
    program_type = db.Column(db.String(100), nullable=False, default="برنامج تثقيفي صحي")
    program_expiry = db.Column(db.String(50), nullable=False)
    qr_code_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'id_number': self.id_number,
            'nationality': self.nationality,
            'profession': self.profession,
            'issue_date': self.issue_date,
            'expiry_date': self.expiry_date,
            'certificate_number': self.certificate_number,
            'program_type': self.program_type,
            'program_expiry': self.program_expiry,
            'qr_code_data': self.qr_code_data,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

