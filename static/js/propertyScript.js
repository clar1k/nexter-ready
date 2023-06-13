const imageInput = document.getElementById('image-input');
    const previewContainer = document.getElementById('preview-container');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    let currentImageIndex = 0;
    let images = [];

    imageInput.addEventListener('change', handleImageUpload);
    prevButton.addEventListener('click', showPreviousImage);
    nextButton.addEventListener('click', showNextImage);

    function handleImageUpload(event) {
      const files = event.target.files;

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        const imageType = /^image\//;

        if (!imageType.test(file.type)) {
          continue;
        }

        const imageURL = URL.createObjectURL(file);
        images.push(imageURL);
      }

      if (images.length > 0) {
        displayImage(currentImageIndex);
      }
    }

    function displayImage(index) {
      previewContainer.innerHTML = '';

      const imageElement = document.createElement('img');
      imageElement.classList.add('preview-image');
      imageElement.onload = function() {
        if (imageElement.width > 20 || imageElement.height > 20) {
          const scaleFactor = Math.min(20 / imageElement.width, 20 / imageElement.height);
          const newWidth = imageElement.width * scaleFactor;
          const newHeight = imageElement.height * scaleFactor;
          imageElement.style.width = newWidth + 'vh';
          imageElement.style.height = newHeight + 'vh';
        }

        previewContainer.appendChild(imageElement);
        updateNavigationButtons();
      };
      imageElement.src = images[index];
    }

    function showPreviousImage() {
      if (currentImageIndex > 0) {
        currentImageIndex--;
        displayImage(currentImageIndex);
      }
    }

    function showNextImage() {
      if (currentImageIndex < images.length - 1) {
        currentImageIndex++;
        displayImage(currentImageIndex);
      }
    }

    function updateNavigationButtons() {
      prevButton.disabled = currentImageIndex === 0;
      nextButton.disabled = currentImageIndex === images.length - 1;
    }