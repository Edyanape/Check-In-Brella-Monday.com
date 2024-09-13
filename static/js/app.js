let videoStream = null;
const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const statusText = document.getElementById('status');
let scanning = false;  // Control de estado para saber si está escaneando

// Función para iniciar la cámara
function startCamera() {
    if (!scanning) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
            .then(stream => {
                video.srcObject = stream;
                videoStream = stream;  // Guardamos el stream para detenerlo luego
                scanning = true;
                statusText.textContent = 'Scanning...';
                scanQRCode();
            })
            .catch(err => {
                console.error('Error accessing camera: ', err);
                statusText.textContent = 'Error accessing camera.';
            });
    } else {
        statusText.textContent = 'Already scanning!';
    }
}

// Función para detener la cámara
function stopCamera() {
    if (videoStream) {
        let tracks = videoStream.getTracks();
        tracks.forEach(track => track.stop());  // Detenemos el stream
        videoStream = null;
        scanning = false;
        video.srcObject = null;  // Detenemos el video en el navegador
        statusText.textContent = 'Camera stopped.';
    } else {
        statusText.textContent = 'Camera is not running!';
    }
}

// Función para capturar el cuadro de video y enviarlo al servidor para el escaneo QR
function scanQRCode() {
    if (!scanning) return;

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convertimos el canvas a un blob y lo enviamos al servidor
    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append('image', blob, 'frame.jpg');

        fetch('/scan_qr', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                statusText.textContent = `QR Code: ${data.qr_data}`;
            } else {
                statusText.textContent = data.message || 'No QR code detected';
            }
        })
        .catch(err => {
            console.error('Error scanning QR code: ', err);
            statusText.textContent = 'Error scanning QR code.';
        });
    });

    // Continuar el escaneo si la cámara sigue activa
    if (scanning) {
        setTimeout(scanQRCode, 1000);
    }
}
