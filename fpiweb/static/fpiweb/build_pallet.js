
let buildPallet = {

    tbody: null,
    scanABoxRow: null,
    totalFormsField: null,

    getNextAvailableBoxFormId: function()
    {
        // text input holds the box number
        let rows = buildPallet.tbody.find("tr");
        let idsInUse = new Set();

        //  input[type='text']
        for(var i=0; i<rows.length; i++) {
            let row = $(rows[i]);
            let hiddenInput = row.find("input[type='hidden']");
            if(hiddenInput.length === 0)
            {
                // This happens when the "Scan a Box" row is present
                continue;
            }

            let id = hiddenInput.attr('id');

            // IDs are of the form id_box_forms-0-box_number
            let pieces = id.split('-');
            if (pieces.length !== 3)
            {
                console.error(`id ${id} split into ${pieces.length} pieces`);
                continue;
            }

            let temp = pieces[1];
            id = Number.parseInt(temp);
            if (Number.isNaN(id)) {
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
        let palletPk = $('#id_pallet-pallet').val();

        if(boxNumber !== '')
            scanData = '';

        $.post(
            '/fpiweb/box/box_form/',
            {
                scanData: scanData,
                boxNumber: boxNumber,
                prefix: prefix,
                palletPk: palletPk,
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

        // If no boxes have been scanned the table contains a row with
        // a message prompting the user to scan a Box.
        buildPallet.scanABoxRow.hide();

        let totalForms = buildPallet.totalFormsField.val();
        totalForms =  Number.parseInt(totalForms);
        totalForms++;

        buildPallet.tbody.prepend(data);
        buildPallet.totalFormsField.val(totalForms);

        let boxFormRows = $('tr.boxItemFormRow');
        let rowCount = boxFormRows.length;
        console.debug(`There are ${rowCount} boxItemFormRows`);
        if(rowCount >= 2)
        {
            let currentRow = $(boxFormRows[0]);
            let priorRow = $(boxFormRows[1]);
            buildPallet.defaultToPriorRowValues(priorRow, currentRow);
        }

        $('button.remove').click(buildPallet.removeBox);
    },

    defaultToPriorRowValues: function(priorRow, currentRow)
    {
        let cellData = [
            {index: 2, selector: 'select'},  // product
            {index: 3, selector: 'select'},  // exp year
            {index: 4, selector: 'input[type="number"]'},  // exp month start
            {index: 5, selector: 'input[type="number"]'}  // exp month end
        ];

        let priorRowCells = priorRow.find('td');
        let currentRowCells = currentRow.find('td');

        for(var i=0; i<cellData.length; i++)
        {
            let cellDatum = cellData[i];
            let value = $(priorRowCells[cellDatum.index])
                .find(cellDatum.selector)
                .val();
            console.debug(
                `priorRow index=${cellDatum.index} value=${value}`
            );
            $(currentRowCells[cellDatum.index])
                .find(cellDatum.selector)
                .val(value);
        }
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

        // scanner setup will attach a click event handler to element
        // with an ID of scanButton
        scanner.setup(
            buildPallet.scanCallback,
            buildPallet.scanRequest
        );
    }
};


// Using JQuery, add event handler for when the DOM is loaded (images,
// etc may still be downloading)
$(document).ready(buildPallet.setup);