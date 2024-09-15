console.log('main.js loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded event fired');
    const uploadForm = document.getElementById('uploadForm');
    const contentTypeSelect = document.getElementById('contentType');
    const textContent = document.getElementById('textContent');
    const fileContent = document.getElementById('fileContent');
    const resultDiv = document.getElementById('result');
    const shortUrlInput = document.getElementById('shortUrl');
    const copyUrlButton = document.getElementById('copyUrl');
    const shareButtons = document.querySelectorAll('.share-btn');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4 hidden';
    if (uploadForm) {
        uploadForm.insertAdjacentElement('afterend', errorDiv);
    }

    if (uploadForm) {
        contentTypeSelect.addEventListener('change', function() {
            if (this.value === 'text') {
                textContent.classList.remove('hidden');
                fileContent.classList.add('hidden');
            } else {
                textContent.classList.add('hidden');
                fileContent.classList.remove('hidden');
            }
        });

        uploadForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            formData.append('content_type', contentTypeSelect.value);

            // Handle tags
            const tagsInput = document.getElementById('tags');
            const tags = tagsInput.value.split(',').map(tag => tag.trim()).filter(tag => tag !== '');
            tags.slice(0, 3).forEach((tag, index) => {
                formData.append('tags', tag);
            });

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.short_url) {
                    const fullUrl = `${window.location.origin}/${data.short_url}`;
                    shortUrlInput.value = fullUrl;
                    resultDiv.classList.remove('hidden');
                    errorDiv.classList.add('hidden');
                } else if (data.error) {
                    throw new Error(data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                errorDiv.textContent = `Error: ${error.message}`;
                errorDiv.classList.remove('hidden');
                resultDiv.classList.add('hidden');
            });
        });
    }

    if (copyUrlButton) {
        copyUrlButton.addEventListener('click', function() {
            navigator.clipboard.writeText(shortUrlInput.value).then(() => {
                alert('URL copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy: ', err);
                alert('Failed to copy URL. Please try again.');
            });
        });
    }

    if (shareButtons) {
        shareButtons.forEach(button => {
            button.addEventListener('click', function() {
                const platform = this.dataset.platform;
                const url = encodeURIComponent(shortUrlInput.value);
                const text = encodeURIComponent('Check out this content on ByteBin!');
                let shareUrl;

                switch (platform) {
                    case 'twitter':
                        shareUrl = `https://twitter.com/intent/tweet?url=${url}&text=${text}`;
                        break;
                    case 'instagram':
                        alert('Instagram sharing is not directly supported. Copy the URL and share it manually.');
                        return;
                    case 'telegram':
                        shareUrl = `https://t.me/share/url?url=${url}&text=${text}`;
                        break;
                    case 'whatsapp':
                        shareUrl = `https://api.whatsapp.com/send?text=${text}%20${url}`;
                        break;
                }

                if (shareUrl) {
                    window.open(shareUrl, '_blank');
                    incrementShareCount(shortUrlInput.value.split('/').pop());
                }
            });
        });
    }

    // Add event listeners for copy buttons on the wall page
    const copyButtons = document.querySelectorAll('.copy-url-btn');
    console.log('Number of copy buttons found:', copyButtons.length);
    
    copyButtons.forEach(button => {
        console.log('Adding click event listener to button');
        button.addEventListener('click', function() {
            console.log('Copy button clicked');
            const url = this.dataset.url;
            console.log('URL to copy:', url);
            navigator.clipboard.writeText(url).then(() => {
                console.log('URL copied successfully');
                // Visual feedback
                const originalColor = this.style.backgroundColor;
                this.style.backgroundColor = '#4CAF50';
                setTimeout(() => {
                    this.style.backgroundColor = originalColor;
                }, 1000);
                alert('URL copied to clipboard!');
            }).catch(err => {
                console.error('Failed to copy: ', err);
                alert('Failed to copy URL. Please try again.');
            });
        });
    });
});

function incrementShareCount(shortUrl) {
    fetch(`/increment_share/${shortUrl}`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Share count incremented. New count:', data.new_share_count);
        } else {
            console.error('Failed to increment share count');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
