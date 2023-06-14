document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('preview-container');
    var prevButton = document.getElementById('prev-button');
    var nextButton = document.getElementById('next-button');
    var images = container.getElementsByTagName('img');
    var currentIndex = 0;
  
    // Функція для відображення поточної фотографії
    function showCurrentImage() {
      for (var i = 0; i < images.length; i++) {
        images[i].style.display = 'none';
      }
      images[currentIndex].style.display = 'block';
    }
  
    // Переключення на попередню фотографію
    prevButton.addEventListener('click', function() {
      if (currentIndex > 0) {
        currentIndex--;
        showCurrentImage();
      }
    });
  
    // Переключення на наступну фотографію
    nextButton.addEventListener('click', function() {
      if (currentIndex < images.length - 1) {
        currentIndex++;
        showCurrentImage();
      }
    });
  
    // Показуємо початкову фотографію
    showCurrentImage();
  
    // Збільшення фото при натисканні на нього
    for (var i = 0; i < images.length; i++) {
      images[i].addEventListener('click', function() {
        this.classList.toggle('zoomed');
      });
    }
  });