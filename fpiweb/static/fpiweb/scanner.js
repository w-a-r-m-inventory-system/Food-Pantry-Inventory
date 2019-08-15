

var scanner = {
    video: document.getElementById('video'),
    scanButton: document.getElementById('scanButton'),
};

function streamToVideoElement(stream)
{
    scanner.video.srcObject = stream;
    scanner.video.play();
}

function logError(err)
{
    console.log(err);
}


function dataURLtoBlob(dataurl)
{
    var arr = dataurl.split(',');
    var mime = arr[0].match(/:(.*?);/)[1];
    var bstr = atob(arr[1]);
    var n = bstr.length;
    var u8arr = new Uint8Array(n);

    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new Blob([u8arr], {type:mime});
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
    var context = canvas.getContext('2d');

    context.drawImage(
        scanner.video,
        0,
        0,
        scanner.video.clientWidth,
        scanner.video.clientHeight
    );
    var scanData = canvas.toDataURL('image/png');
    console.log(scanData);

    // This block and dataURLtoBlob taken from:
    // https://stackoverflow.com/questions/6850276/how-to-convert-dataurl-to-file-object-in-javascript
    // var blob = dataURLtoBlob(scanData);

    // Using js.cookie.js Cookies class to get csrftoken as per:
    // https://docs.djangoproject.com/en/2.2/ref/csrf/
    // var csrftoken = Cookies.get('csrftoken');

    console.log("scanData is " + Number(scanData.length).toLocaleString() + " characters in length");

    console.log("sending AJAX request");
    $.ajax({
        url: '/fpiweb/scanner/',
        method: 'post',
        data: {
            'scanData': scanData
        }
    });


    // var formData = new FormData();
    // formData.append("csrfmiddlewaretoken", csrftoken);
    // formData.append("file", blob, "hello.txt");


    // var xhr = new XMLHttpRequest();
    // var async = true;
    // xhr.addEventListener('load', processScanResponse);
    // xhr.open('POST', , async);
    // // xhr.onload = processScanResponse;
    // xhr.send(formData);
    // // end of block

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






/*
* function setup()
{
    scanner.width = window.innerWidth || document.body.clientWidth;
    scanner.height = window.innerHeight || document.body.clientHeight;

    if(scanner.width > scanner.height)
    {
        // landscape
        scanner.height = scanner.height / 2.0;
        scanner.width = 4 * scanner.height / 3.0;
    }
    else
    {
        // portrait
        scanner.height = scanner.width * 0.75;
    }

    scanner.video.setAttribute('width', scanner.width);
    scanner.video.setAttribute('height', scanner.height);

    navigator.mediaDevices
        .getUserMedia({video: true, audio: false})
        .then(streamToVideoElement)
        .catch(logError);

    scanner.scanButton.addEventListener('click', scan);
}

* */