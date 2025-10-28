// API Base URL
const API_BASE = '/api';

// DOM Elements
const issueForm = document.getElementById('issueForm');
const verifyIdForm = document.getElementById('verifyIdForm');
const verifyQrForm = document.getElementById('verifyQrForm');
const certificatesTableBody = document.getElementById('certificatesTableBody');
const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
const resultModalTitle = document.getElementById('resultModalTitle');
const resultModalBody = document.getElementById('resultModalBody');

// Set today's date as default for issue date
document.getElementById('issue_date').value = new Date().toISOString().split('T')[0];

// Set expiry date to one year from today
const expiryDate = new Date();
expiryDate.setFullYear(expiryDate.getFullYear() + 1);
document.getElementById('expiry_date').value = expiryDate.toISOString().split('T')[0];

// Issue Certificate Form Handler
issueForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        id_number: document.getElementById('id_number').value,
        nationality: document.getElementById('nationality').value,
        profession: document.getElementById('profession').value,
        issue_date: document.getElementById('issue_date').value,
        expiry_date: document.getElementById('expiry_date').value
    };

    try {
        const response = await fetch(`${API_BASE}/certificates`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (response.ok) {
            showModal('تم إصدار الشهادة بنجاح', `
                <div class="alert alert-success">
                    <h6>تم إنشاء الشهادة بنجاح!</h6>
                    <p><strong>رقم الشهادة:</strong> ${data.certificate.certificate_number}</p>
                    <p><strong>الاسم:</strong> ${data.certificate.name}</p>
                    <p><strong>رقم الهوية:</strong> ${data.certificate.id_number}</p>
                    <a href="${API_BASE}/certificates/${data.certificate.id_number}/pdf" 
                       class="btn btn-primary mt-2" target="_blank">
                        <i class="fas fa-download me-2"></i>تحميل الشهادة PDF
                    </a>
                </div>
            `);
            issueForm.reset();
            // Reset default dates
            document.getElementById('issue_date').value = new Date().toISOString().split('T')[0];
            document.getElementById('expiry_date').value = expiryDate.toISOString().split('T')[0];
            document.getElementById('nationality').value = 'سعودي';
            document.getElementById('profession').value = 'عامل';
        } else {
            showModal('خطأ في إصدار الشهادة', `
                <div class="alert alert-danger">
                    <p>${data.error}</p>
                </div>
            `);
        }
    } catch (error) {
        showModal('خطأ في الاتصال', `
            <div class="alert alert-danger">
                <p>حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.</p>
            </div>
        `);
    }
});

// Verify by ID Form Handler
verifyIdForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const idNumber = document.getElementById('verify_id_number').value;

    try {
        const response = await fetch(`${API_BASE}/certificates/${idNumber}/verify`);
        const data = await response.json();

        if (response.ok && data.valid) {
            const cert = data.certificate;
            showModal('الشهادة صحيحة', `
                <div class="alert alert-success">
                    <h6><i class="fas fa-check-circle me-2"></i>الشهادة صحيحة وسارية المفعول</h6>
                    <hr>
                    <p><strong>الاسم:</strong> ${cert.name}</p>
                    <p><strong>رقم الهوية:</strong> ${cert.id_number}</p>
                    <p><strong>رقم الشهادة:</strong> ${cert.certificate_number}</p>
                    <p><strong>الجنسية:</strong> ${cert.nationality}</p>
                    <p><strong>المهنة:</strong> ${cert.profession}</p>
                    <p><strong>تاريخ الإصدار:</strong> ${cert.issue_date}</p>
                    <p><strong>تاريخ الانتهاء:</strong> ${cert.expiry_date}</p>
                    <a href="${API_BASE}/certificates/${cert.id_number}/pdf" 
                       class="btn btn-primary mt-2" target="_blank">
                        <i class="fas fa-download me-2"></i>تحميل الشهادة PDF
                    </a>
                </div>
            `);
        } else {
            showModal('الشهادة غير صحيحة', `
                <div class="alert alert-danger">
                    <h6><i class="fas fa-times-circle me-2"></i>الشهادة غير موجودة أو غير صحيحة</h6>
                    <p>لم يتم العثور على شهادة بهذا الرقم في قاعدة البيانات.</p>
                </div>
            `);
        }
    } catch (error) {
        showModal('خطأ في التحقق', `
            <div class="alert alert-danger">
                <p>حدث خطأ في الاتصال بالخادم. يرجى المحاولة مرة أخرى.</p>
            </div>
        `);
    }
});

// Verify QR Form Handler
verifyQrForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('pdf_file');
    const file = fileInput.files[0];

    if (!file) {
        showModal('خطأ', `
            <div class="alert alert-warning">
                <p>يرجى اختيار ملف PDF للفحص.</p>
            </div>
        `);
        return;
    }

    const formData = new FormData();
    formData.append('pdf_file', file);

    try {
        const response = await fetch(`${API_BASE}/verify-qr`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.valid) {
            const cert = data.certificate;
            showModal('رمز QR صحيح', `
                <div class="alert alert-success">
                    <h6><i class="fas fa-qrcode me-2"></i>رمز QR صحيح والشهادة سارية المفعول</h6>
                    <hr>
                    <p><strong>الاسم:</strong> ${cert.name}</p>
                    <p><strong>رقم الهوية:</strong> ${cert.id_number}</p>
                    <p><strong>رقم الشهادة:</strong> ${cert.certificate_number}</p>
                    <p><strong>الجنسية:</strong> ${cert.nationality}</p>
                    <p><strong>المهنة:</strong> ${cert.profession}</p>
                    <p><strong>تاريخ الإصدار:</strong> ${cert.issue_date}</p>
                    <p><strong>تاريخ الانتهاء:</strong> ${cert.expiry_date}</p>
                </div>
            `);
        } else {
            showModal('رمز QR غير صحيح', `
                <div class="alert alert-danger">
                    <h6><i class="fas fa-times-circle me-2"></i>رمز QR غير صحيح أو الشهادة غير موجودة</h6>
                    <p>${data.message || 'لم يتم العثور على رمز QR صحيح في الملف.'}</p>
                </div>
            `);
        }
    } catch (error) {
        showModal('خطأ في فحص رمز QR', `
            <div class="alert alert-danger">
                <p>حدث خطأ في فحص رمز QR. يرجى التأكد من أن الملف صحيح والمحاولة مرة أخرى.</p>
            </div>
        `);
    }
});

// Load certificates when list tab is clicked
document.getElementById('list-tab').addEventListener('click', loadCertificates);

// Load certificates function
async function loadCertificates() {
    try {
        const response = await fetch(`${API_BASE}/certificates`);
        const data = await response.json();

        if (response.ok) {
            displayCertificates(data.certificates);
        } else {
            certificatesTableBody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-danger">
                        خطأ في تحميل البيانات: ${data.error}
                    </td>
                </tr>
            `;
        }
    } catch (error) {
        certificatesTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-danger">
                    خطأ في الاتصال بالخادم
                </td>
            </tr>
        `;
    }
}

// Display certificates in table
function displayCertificates(certificates) {
    if (certificates.length === 0) {
        certificatesTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center text-muted">
                    لا توجد شهادات مسجلة
                </td>
            </tr>
        `;
        return;
    }

    certificatesTableBody.innerHTML = certificates.map(cert => `
        <tr>
            <td>${cert.name}</td>
            <td>${cert.id_number}</td>
            <td>${cert.certificate_number}</td>
            <td>${cert.issue_date}</td>
            <td>${cert.expiry_date}</td>
            <td>
                <a href="${API_BASE}/certificates/${cert.id_number}/pdf" 
                   class="btn btn-sm btn-primary" target="_blank">
                    <i class="fas fa-download"></i> PDF
                </a>
            </td>
        </tr>
    `).join('');
}

// Show modal function
function showModal(title, body) {
    resultModalTitle.textContent = title;
    resultModalBody.innerHTML = body;
    resultModal.show();
}

