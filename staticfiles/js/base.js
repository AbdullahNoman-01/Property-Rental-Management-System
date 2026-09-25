const menuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');
   menuToggle.addEventListener('click', function () {
      navMenu.classList.toggle('active');
   });