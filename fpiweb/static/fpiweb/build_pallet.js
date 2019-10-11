
function getNextAvailableBoxFormId(tbody)
{
    // text input holds the box number
    let textInputs = tbody.find("tr input[type='text']");

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
}

function addBoxForm(boxData)
{
    let tbody = $('table#boxTable>tbody');

    let formId = getNextAvailableBoxFormId(tbody);
    console.debug(`formId is ${formId}`);

    tbody.prepend(
        `<tr> \
          <td> \ 
            <div class="form-group"> \
              <label class="sr-only" \
                     for="id_box_forms-${formId}-box_number">Box number</label> \
              <input type="text" \
                     name="box_forms-${formId}-box_number" \ 
                     maxlength="8" \
                     minlength="8" \
                     class="form-control" \
                     placeholder="Box number" \ 
                     title="" \ 
                     disabled="" \
                     id="id_box_forms-${formId}-box_number"> \
            </div> \
          </td> \
          <td></td> \
          <td></td> \
        </tr>`
    );
}

function buildPalletScanCallback(data)
{
    console.log("buildPalletScanCallback called");
    if(!data.success)
    {
        alert('scan failed');
        return;
    }

    hideModal();
    addBoxForm(data.data);
}

function handle_document_ready()
{
    scanner.setup(buildPalletScanCallback);
}

// Using JQuery, add event handler for when the DOM is loaded (images,
// etc may still be downloading)
$(document).ready(handle_document_ready);