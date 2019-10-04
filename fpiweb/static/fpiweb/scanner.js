

var video = document.getElementById('video');

function streamToVideoElement(stream)
{
    video.srcObject = stream;
    video.play();
}

function logError(err)
{
    console.log(err);
}

function processScanResponse(){

    // XMLHttpRequest
    var xhr = this;

    console.log("this.responseText is " + this.responseText);
    console.log("this.responseType is '" + this.responseType + "'");


    console.log("members of this are:");
    for(var symbol in this)
    // for(var symbol in e)
    {
        console.log(symbol);
    }

}


function scan(event)
{
    var canvas = document.createElement('canvas');
    canvas.width = video.clientWidth;
    canvas.height = video.clientHeight;

    var context = canvas.getContext('2d');

    context.drawImage(
        video,
        0,
        0,
        video.clientWidth,
        video.clientHeight
    );
    var scanData = canvas.toDataURL('image/png');

    console.log("scanData is " + Number(scanData.length).toLocaleString() + " characters in length");

    console.log("sending AJAX request");
    $.ajax({
        url: '/fpiweb/scanner/',
        method: 'post',
        data: {
            'scanData': scanData,
            'boxNumber': document.getElementById('boxNumber').value
        }
    });

    event.preventDefault();
}

/*
    https://docs.djangoproject.com/en/2.2/ref/csrf/#setting-the-token-on-the-ajax-request
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function beforeSend(xml_http_request, settings)
{
    if(csrfSafeMethod(settings.type))
        return;

    if(this.crossDomain)
        return;

    var csrftoken = Cookies.get('csrftoken');
    xml_http_request.setRequestHeader("X-CSRFToken", csrftoken);
}


function setup_scanner()
{
    navigator.mediaDevices
        .getUserMedia({video: true, audio: false})
        .then(streamToVideoElement)
        .catch(logError);

    $.ajaxSetup({beforeSend: beforeSend});

    $('#scanButton').click(scan);
}

