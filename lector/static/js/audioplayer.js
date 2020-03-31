

function setup(event) {
    var endTime = Math.floor(document.getElementById("audioplayer").duration);
    $("#slider").attr('max',endTime);
    $("#slider").attr('min','0');
    $("#slider").attr('value','0');
    $("#slider").attr('step','0.1');
    
    document.getElementById("end-time").innerHTML = convertToTimeString(endTime);

    document.getElementById("slider").addEventListener('input',function() {
        pause();
        console.log(parseFloat(this.value));
        this.setAttribute('value',this.value);
        document.getElementById("start-time").innerHTML = convertToTimeString(this.value);
    });

    document.getElementById("slider").addEventListener("change",function() {
        document.getElementById("audioplayer").currentTime = parseFloat(this.value);
        console.log(parseFloat(this.value));
        //play();
    });


    document.getElementById("audioplayer").addEventListener('timeupdate', function() {
        document.getElementById("slider").value = document.getElementById("audioplayer").currentTime;
        var time = document.getElementById("audioplayer").currentTime;
        document.getElementById("start-time").innerHTML = convertToTimeString(time);
    });

    $("#play-btn").click(function() {
        console.log("clicked!");
        playPause();
    });
}

function playPause() {
    if ($("#play-btn").attr("data-id") == "paused") {
        play();
    } else {
        pause();
    }
}

function play() {
    $("#play-btn").attr("data-id","playing");
    $("#play-btn").find('i').removeClass('fa-play');
    $("#play-btn").find('i').addClass('fa-pause');
    document.getElementById("audioplayer").play();
}

function pause() {
    $("#play-btn").attr("data-id","paused");
    $("#play-btn").find('i').removeClass('fa-pause');
    $("#play-btn").find('i').addClass('fa-play');
    document.getElementById("audioplayer").pause();
}

function convertToTimeString(time) {
    var date = new Date(null);
    date.setSeconds(time);
    return date.toISOString().substr(11, 8);
}
