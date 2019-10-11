
let scanner = {
    video: document.getElementById('video'),
    callback: null,
    requestMethod: null,

    logError: function(err)
    {
        console.log(err);
    },

    streamToVideoElement: function(stream)
    {
        scanner.video.srcObject = stream;
        scanner.video.play();
    },

    setup: function(callback, requestMethod=null)
    {
        navigator.mediaDevices
            .getUserMedia({video: true, audio: false})
            .then(scanner.streamToVideoElement)
            .catch(scanner.logError);

        $.ajaxSetup({beforeSend: beforeSend});

        scanner.callback = callback;
        if(requestMethod){
            scanner.requestMethod = requestMethod;
        }else{
            scanner.requestMethod = scanner.defaultRequestMethod;
        }

        $('#scanButton').click(scanner.scan);
    },

    defaultRequestMethod: function(scanData, boxNumber, callback)
    {
        $.post(
            '/fpiweb/scanner/',
            {
                'scanData': scanData,
                'boxNumber': boxNumber,
            },
            callback,
        );
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

        scanner.requestMethod(scanData, boxNumber, scanner.callback);

        event.preventDefault();
    },

    hideModal: function()
    {
        let scannerModal = $('div#scannerModal');
        scannerModal.modal('hide');

        $('div.modal-backdrop').remove();
    }
};





