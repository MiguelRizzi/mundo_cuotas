
const navLinks = document.querySelectorAll('.nav-link');
const currentPath = window.location.pathname;

navLinks.forEach(link => {
  const linkPath = link.getAttribute('href');
      if (currentPath === linkPath) {
    link.classList.add('active');
  } else {
    link.classList.remove('active');
  }
})();
    

const yearElement = document.getElementById("year");
const currentYear = new Date().getFullYear();
yearElement.textContent = currentYear;
