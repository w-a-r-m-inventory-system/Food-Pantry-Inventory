
let scanner = {
    video: document.getElementById('video'),
    callback: null,
    defaultUrl: '/fpiweb/scanner/',
    alternateUrl: null,

    logError: function(err)
    {
        console.log(err);
    },

    streamToVideoElement: function(stream)
    {
        scanner.video.srcObject = stream;
        scanner.video.play();
    },

    setup: function(callback)
    {
        navigator.mediaDevices
            .getUserMedia({video: true, audio: false})
            .then(scanner.streamToVideoElement)
            .catch(scanner.logError);

        $.ajaxSetup({beforeSend: beforeSend});

        scanner.callback = callback;

        $('#scanButton').click(scanner.scan);
    },

    scan: function(event)
    {
        let canvas = document.createElement('canvas');
        canvas.width = scanner.video.clientWidth;
        canvas.height = scanner.video.clientHeight;

        let context = canvas.getContext('2d');

        context.drawImage(
            scanner.video,
            0,
            0,
            scanner.video.clientWidth,
            scanner.video.clientHeight
        );

        let scanData = canvas.toDataURL('image/png');
        let dataLength = Number(scanData.length).toLocaleString();
        console.log(`scanData is ${dataLength} characters in length`);

        let boxNumber = document.getElementById('boxNumber').value;

        $.post(
            scanner.defaultUrl,
             {
                'scanData': scanData,
                'boxNumber': boxNumber,
            },
            scanner.callback,
        );

        event.preventDefault();
    }
};












function hideModal()
{
    let scannerModal = $('div#scannerModal');
    scannerModal.modal('hide');

    $('div.modal-backdrop').remove();
}

