// [1] Set an Array for all icons and another one for all buttons
var collapsable_icons = Array.from(document.querySelectorAll('button i'));
var buttons = Array.from(document.querySelectorAll('button.btn-genre'));

// Add 'click' event for every icon and button
for (icon of collapsable_icons) {
    icon.addEventListener('click', clickIconGenre);
}

for (button of buttons) {
    button.addEventListener('click', clickButtonGenre);
}

// [5] Change icon class
function changeIcon(n, status) {
    if (status == 4) {
        collapsable_icons[n].className = "fas fa-chevron-down";
    } else {
        collapsable_icons[n].className = "fas fa-chevron-up";
    }
}
// [3] Get status if is collpased show or not
function getStatus(n) {
    status = buttons[n].className.split(' ').length;
    changeIcon(n, status);
}

// [2] Get index 'n' of element in the list
function clickIconGenre(event) {
    n = collapsable_icons.indexOf(event.srcElement);
    getStatus(n);
}

function clickButtonGenre(event) {
    n = buttons.indexOf(event.srcElement);
    getStatus(n);
}