var likeIcons = document.querySelectorAll(".home__like");
    likeIcons.forEach(function(likeIcon) {
        likeIcon.addEventListener("click", function() {
            this.classList.toggle("liked");
        });
    });