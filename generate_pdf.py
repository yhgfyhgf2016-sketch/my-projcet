from fpdf import FPDF
import qrcode

class PDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

def create_certificate_pdf(output_path, certificate_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr_data = f"Name: {certificate_data['name']}\nID: {certificate_data['id_number']}\nIssue Date: {certificate_data['issue_date']}\nExpiry Date: {certificate_data['expiry_date']}"
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    qr_code_path = "temp_qr_code.png"
    img.save(qr_code_path)

    pdf = PDF()
    pdf.add_page()
    pdf.image('certificate_template-1.png', 0, 0, 210, 297)
    pdf.add_font("Tajawal", "", "Tajawal-Regular.ttf", uni=True)
    pdf.set_font("Tajawal", "", 12)
    # تحديد مواضع البيانات حسب القالب الجديد (بوحدة النقاط)
    pdf.set_xy(150, 80)  # رقم الهوية
    pdf.cell(0, 10, certificate_data["id_number"], 0, 1)
    
    pdf.set_xy(80, 80)  # الجنسية - سنضع قيمة افتراضية
    pdf.cell(0, 10, "سعودي", 0, 1)
    
    pdf.set_xy(150, 110)  # رقم الشهادة الصحية
    pdf.cell(0, 10, certificate_data["id_number"], 0, 1)
    
    pdf.set_xy(80, 110)  # المهنة - سنضع قيمة افتراضية
    pdf.cell(0, 10, "عامل", 0, 1)
    
    pdf.set_xy(150, 140)  # تاريخ إصدار الشهادة الصحية
    pdf.cell(0, 10, certificate_data["issue_date"], 0, 1)
    
    pdf.set_xy(80, 140)  # تاريخ نهاية الشهادة الصحية
    pdf.cell(0, 10, certificate_data["expiry_date"], 0, 1)
    
    pdf.set_xy(150, 170)  # نوع البرنامج التثقيفي
    pdf.cell(0, 10, "برنامج تثقيفي صحي", 0, 1)
    
    pdf.set_xy(80, 170)  # تاريخ انتهاء البرنامج التثقيفي
    pdf.cell(0, 10, certificate_data["expiry_date"], 0, 1)
    
    # وضع رمز QR في الزاوية اليسرى السفلى
    pdf.image(qr_code_path, 20, 250, 30, 30)

    pdf.add_page()
    pdf.image('certificate_template-2.png', 0, 0, 210, 297)

    pdf.output(output_path)

if __name__ == '__main__':
    # Example usage (will be replaced with actual data)
    certificate_data = {
        'name': 'اسم حامل الشهادة',
        'id_number': 'رقم الهوية',
        'issue_date': 'تاريخ الإصدار',
        'expiry_date': 'تاريخ الانتهاء'
    }
    create_certificate_pdf('sample_certificate.pdf', certificate_data)


