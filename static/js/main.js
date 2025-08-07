// Image upload preview functionality
document.addEventListener('DOMContentLoaded', function() {
    const imageUpload = document.getElementById('image-upload');
    const imagePreview = document.getElementById('image-preview');
    
    if (imageUpload && imagePreview) {
        imageUpload.addEventListener('change', function() {
            // Clear the preview
            imagePreview.innerHTML = '';
            
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.alt = 'Preview';
                    
                    // Add a remove button
                    const removeBtn = document.createElement('button');
                    removeBtn.type = 'button';
                    removeBtn.className = 'remove-image-btn';
                    removeBtn.textContent = 'Remove';
                    removeBtn.addEventListener('click', function() {
                        imagePreview.innerHTML = '';
                        imageUpload.value = '';
                    });
                    
                    // Add both to the preview
                    imagePreview.appendChild(img);
                    imagePreview.appendChild(removeBtn);
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
});
