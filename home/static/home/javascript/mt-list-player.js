var icons = Array.from(document.querySelectorAll('i.far'));
var previews = Array.from(document.querySelectorAll('audio'));
var playing = -1;

for (icon of icons) {
    icon.addEventListener("click", getIcon); 
}

for (preview of previews) {
    preview.addEventListener("ended", previewEnd); 
}

function setPlay(n) {
    previews[n].play();
    playing = n
    icons[n].className = "far fa-pause-circle fs-6 icon-player";
}

function setPause(n) {
    previews[n].pause();
    icons[n].className = "far fa-play-circle fs-6 icon-player";
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

function previewEnd(event) {
    n = previews.indexOf(event.srcElement);
    setPause(n)
}