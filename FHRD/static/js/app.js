const videoEl = document.getElementById('web-vid');

const startWebcam = () => {
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(stream => { videoEl.srcObject = stream })
            .catch(err => { console.log('Something went wrong ==>', err) })
    }
}

const stopWebcam = () => {
    var stream = videoEl.srcObject;
    var tracks = stream.getTracks();

    for (var i = 0; i < tracks.length; i++) {
        var track = tracks[i]
        track.stop()
    }
    videoEl.srcObject = null
}