var loadingIcon = document.querySelector(".loading");
loadingIcon.style.display = "block";

window.addEventListener("load", function() {
    var loadingIcon = document.querySelector(".loading");
    loadingIcon.style.display = "none";
  });

  window.addEventListener('load', function() {
    var content = document.querySelector('.content');
    content.style.display = 'none';
  });
  
  window.addEventListener('load', function() {
    var loadingOverlay = document.querySelector('.loading-overlay');
    loadingOverlay.addEventListener('animationend', function() {
      loadingOverlay.remove();
    });
  });
  