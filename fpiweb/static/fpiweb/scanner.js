
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

    defaultRequestFailed: function(jqXHR, textStatus, errorThrown)
    {
        let error = jqXHR.responseText;
        console.error(error);
        alert(error)
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
        ).fail(scanner.defaultRequestFailed);
    },

    scan: function(event)
    {
        event.preventDefault();
        event.stopPropagation();

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

        let boxNumberField = document.getElementById('boxNumber')
        let boxNumber = boxNumberField.value;
        boxNumberField.value = '';

        scanner.requestMethod(scanData, boxNumber, scanner.callback);
    },

    hideModal: function()
    {
        let scannerModal = $('div#scannerModal');
        scannerModal.modal('hide');

        $('div.modal-backdrop').remove();
    }
};





