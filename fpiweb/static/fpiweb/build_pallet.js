
let buildPallet = {

    tbody: null,

    getNextAvailableBoxFormId: function()
    {
        // text input holds the box number
        let textInputs = buildPallet.tbody.find("tr input[type='text']");

        let idsInUse = new Set();
        for(var i=0; i<textInputs.length; i++)
        {
            let textInput = textInputs[i];
            let id = textInput.id;

            // IDs are of the form id_box_forms-0-box_number
            let pieces = id.split('-');
            if(pieces.length !== 3)
            {
                console.error(`id ${id} split into ${pieces.length} pieces`);
                continue;
            }

            let temp = pieces[1];
            id = Number.parseInt(temp);
            if(Number.isNaN(id))
            {
                console.error(`'${temp}' is not an integer`);
                continue;
            }

            idsInUse.add(id);
        }

        let j = 0;
        while(idsInUse.has(j))
        {
            j++;
        }
        return j;
    },

    scanRequest: function(scanData, boxNumber, callback)
    {
        let nextFormId = buildPallet.getNextAvailableBoxFormId();
        let prefix = `box_forms-${nextFormId}`;

        $.post(
            '/fpiweb/box/box_form/',
            {
                scanData: scanData,
                boxNumber: boxNumber,
                prefix: prefix,
            },
            callback,
            'html'
        )
    },

    scanCallback: function(data, textStatus, jqXHR)
    {
        console.log("buildPallet.scanCallback called");
        if(jqXHR.status >= 400)
        {
            alert(jqXHR.responseText);
            return;
        }

        buildPallet.tbody.prepend(data);

        scanner.hideModal();
    },

    setup: function()
    {
        buildPallet.tbody = $('table#boxTable>tbody');
        scanner.setup(
            buildPallet.scanCallback,
            buildPallet.scanRequest
        );
    }
};








// Using JQuery, add event handler for when the DOM is loaded (images,
// etc may still be downloading)
$(document).ready(buildPallet.setup);