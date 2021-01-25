var icons = Array.from(document.querySelectorAll('i.far'));
var previews = Array.from(document.querySelectorAll('audio'));
var playing = -1;

for (icon of icons) {
    icon.addEventListener("click", getIcon); 
}

function setPlay(n) {
    previews[n].play();
    playing = n
    icons[n].className = "far fa-pause-circle fs-5";
}

function setPause(n) {
    previews[n].pause();
    icons[n].className = "far fa-play-circle fs-5";
}

function startPlaying(n) {
    if (playing < 0) {
        setPlay(n);
    } else {
        setPause(playing);
        setPlay(n);
    }
}

function getIcon(event) {
    n = icons.indexOf(event.srcElement);
    if (previews[n].paused) {
        startPlaying(n);
    } else {
        setPause(n);
    }
}