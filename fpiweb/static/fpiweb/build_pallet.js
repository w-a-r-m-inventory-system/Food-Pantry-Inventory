
let buildPallet = {

    tbody: null,
    scanABoxRow: null,
    totalFormsField: null,

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

    scanErrorHandler: function(jqXHR, textStatus, errorThrown)
    {
        console.error(jqXHR.responseText);
        alert(jqXHR.responseText);
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
        ).fail(buildPallet.scanErrorHandler);
    },

    scanCallback: function(data, textStatus, jqXHR)
    {
        console.log("buildPallet.scanCallback called");
        scanner.hideModal();
        if(jqXHR.status >= 400)
        {
            buildPallet.scanErrorHandler(jqXHR, textStatus, null);
            return;
        }

        buildPallet.tbody.prepend(data);
        buildPallet.scanABoxRow.hide();
        buildPallet.totalFormsField.val(
            Number.parseInt(buildPallet.totalFormsField.val()) + 1
        );
        $('button.remove').click(buildPallet.removeBox);
    },

    removeBox: function(event)
    {
        event.preventDefault();
        event.stopPropagation();

        let button = $(event.target);
        let row = button.parents('tr');
        row.remove();
        let totalForms =  Number.parseInt(buildPallet.totalFormsField.val());
        totalForms--;
        buildPallet.totalFormsField.val(totalForms);
        if(totalForms === 0)
            buildPallet.scanABoxRow.show();
    },

    setup: function()
    {
        buildPallet.tbody = $('table#boxTable>tbody');
        buildPallet.scanABoxRow = $('#scanABoxRow');
        buildPallet.totalFormsField = $('#id_box_forms-TOTAL_FORMS');

        $('button.remove').click(buildPallet.removeBox);

        scanner.setup(
            buildPallet.scanCallback,
            buildPallet.scanRequest
        );
    }
};








// Using JQuery, add event handler for when the DOM is loaded (images,
// etc may still be downloading)
$(document).ready(buildPallet.setup);