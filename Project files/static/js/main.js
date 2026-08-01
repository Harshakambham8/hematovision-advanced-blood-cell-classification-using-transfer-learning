// Main JavaScript for HematoVision Interactive Upload & Validation
document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const imagePreview = document.getElementById('image-preview');
    const fileNameSpan = document.getElementById('file-name');
    const uploadForm = document.getElementById('upload-form');
    const spinnerOverlay = document.getElementById('spinner-overlay');

    if (!dropZone || !fileInput) return;

    // Click to select file
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag events
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        }, false);
    });

    // Drop file handler
    dropZone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            fileInput.files = files;
            handleFileSelect(files[0]);
        }
    });

    // File input change handler
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        // Validate file type
        const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff'];
        if (!allowedTypes.includes(file.type)) {
            alert('Invalid file format. Please upload a PNG, JPG, BMP, or TIFF image.');
            fileInput.value = '';
            return;
        }

        // Validate file size (16MB max)
        if (file.size > 16 * 1024 * 1024) {
            alert('File size exceeds 16MB limit.');
            fileInput.value = '';
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            fileNameSpan.textContent = file.name;
            previewContainer.classList.remove('d-none');
        };
        reader.readAsDataURL(file);
    }

    // Show spinner on form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', () => {
            if (spinnerOverlay) {
                spinnerOverlay.classList.remove('d-none');
            }
        });
    }
});
