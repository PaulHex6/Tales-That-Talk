let isPlaying = false;
let audio = null;

function playPause() {
  if (!isPlaying) {
    audio = new Audio('/path/to/tts/audio/file');
    audio.play();
    isPlaying = true;
  } else {
    audio.pause();
    isPlaying = false;
  }
}

audio.addEventListener("ended", () => {
  isPlaying = false;
});
