document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.querySelector('.upload-button');
    const fileInput = document.getElementById('file-input');
    const submitButton = document.getElementById('submit-button');
    const webcamButton = document.querySelector('.webcam-button');
    const video = document.getElementById('video');
    const stopCamButton = document.getElementById('stop-cam-button');
    let stream = null;

    function startCamera() {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (mediaStream) {
                    stream = mediaStream;
                    video.srcObject = stream;
                    video.style.display = 'block'; // Show the video element
                    // fetch('/start_webcam')
                    //     .then(response => response.json())
                    //     .then(data => console.log('Response:', data));
                })
                .catch(function (error) {
                    console.log("Something went wrong!", error);
                });
        }
    }

    function stopCamera() {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.style.display = 'none'; // Hide the video element
            // fetch('/stop_webcam')
            //     .then(response => response.json())
            //     .then(data => console.log('Response:', data))
            //     .catch(error => console.error('Error stopping webcam:', error));
        }
    }

    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            submitButton.click();  // Automatically submit the form when a file is chosen
        }
    });

    webcamButton.addEventListener('click', startCamera);
    stopCamButton.addEventListener('click', stopCamera);
});
