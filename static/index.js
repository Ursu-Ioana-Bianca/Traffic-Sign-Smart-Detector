/* Logica pentru butoanele de upload si webcam */
document.addEventListener("DOMContentLoaded", function () {
    const uploadButton = document.querySelector('.upload-button');
    const fileInput = document.getElementById('file-input');
    const submitButton = document.getElementById('submit-button');
    let stream = null;

    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    fileInput.addEventListener('change', function () {
        if (this.files.length > 0) {
            submitButton.click();  // Automatically submit the form when a file is chosen
        }
    });

    const webcamButton = document.querySelector('.webcam-button');
    const video = document.getElementById('video');

    webcamButton.addEventListener('click', function () {
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (mediaStream) {
                    stream = mediaStream;
                    video.srcObject = stream;
                    video.style.display = 'block'; // Show the video element
                })
                .catch(function (error) {
                    console.log("Something went wrong!");
                });
        }
    });

    const stopCamButton = document.getElementById('stop-cam-button');
    stopCamButton.addEventListener('click', function () {
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.style.display = 'none'; // Hide the video element
        }
    });

});
