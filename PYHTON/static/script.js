document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission

    const form = event.target;
    const formData = new FormData(form);
    const xhr = new XMLHttpRequest();

    // Update the progress bar
    xhr.upload.addEventListener('progress', function (event) {
        if (event.lengthComputable) {
            const percentComplete = Math.round((event.loaded / event.total) * 100);
            const progressBar = document.getElementById('progressBar');
            const progressText = document.getElementById('progressText');

            progressBar.style.width = percentComplete + '%';
            progressText.textContent = percentComplete + '%';
        }
    });

    // Reset progress bar on completion
    xhr.addEventListener('load', function () {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');

        progressBar.style.width = '100%';
        progressText.textContent = 'Upload Complete!';
    });

    // Handle errors
    xhr.addEventListener('error', function () {
        alert('An error occurred while uploading the files.');
    });

    // Configure the request
    xhr.open('POST', form.action, true);
    xhr.send(formData);
});
