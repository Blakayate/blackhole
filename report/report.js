function toggleIcon(x) {
    x.classList.toggle('fa-eye-slash');
    x.classList.toggle('fa-eye');

    var el = x.parentNode.parentNode.querySelectorAll("[class^=section-content]");

    el[0].classList.toggle('disabled');
}

function toggleSubIcon(x) {
    x.classList.toggle('fa-eye-slash');
    x.classList.toggle('fa-eye');

    var el = x.parentNode.parentNode.querySelectorAll("[class^=service-subcontent]");

    el[0].classList.toggle('disabled');
}