var icons = Array.from(document.querySelectorAll('i.far'));
var previews = Array.from(document.querySelectorAll('audio'));
var playing = -1;

for (icon of icons) {
    icon.addEventListener("click", getIcon); 
}

function setPlayer(n) {
    if (playing < 0) {
        previews[n].play();
        playing = n
        icons[n].className = "far fa-pause-circle fs-5";
    } else {
        previews[playing].pause();
        icons[playing].className = "far fa-play-circle fs-5";
        previews[n].play();
        playing = n;
        icons[n].className = "far fa-pause-circle fs-5";
    }
}

function getIcon(event) {
    n = event.srcElement.id.split('-')[1];
    if (previews[n-1].paused) {
        setPlayer(n-1);
    } else {
        previews[n-1].pause();
        icons[n-1].className = "far fa-play-circle fs-5";
    }
}


