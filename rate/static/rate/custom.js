// Following function will rearranges the table columns as per the position field
function rearrangeTableColumns() {
    // Store the positions in array
    const colOrder = {}
    document.querySelectorAll("#TemplateTable > thead > tr > th").forEach((element, index) => {
        colOrder[index] = parseFloat(element.getAttribute("position"));
    });

    // Sort table header based on the values stored in the array
    const headerRows = document.querySelectorAll("#TemplateTable > thead > tr ").forEach((headerRow) => {
        const columns = headerRow.children;
        let sortedColumns = Array.from(columns).sort((a, b) => {
            let indexA = Array.from(columns).indexOf(a);
            let indexB = Array.from(columns).indexOf(b);
            return colOrder[indexA] - colOrder[indexB];
        });
        headerRow.innerHTML = ""; // Remove content from the row
        sortedColumns.forEach((column) => {
            headerRow.append(column); // Add content to the row from the sorted array
        });
    });

    // Sort table rows based on the values stored in the array
    const tableRows = document.querySelectorAll("#TemplateTable > tbody > tr ").forEach((tableRow) => {
        const columns = tableRow.children;
        let sortedColumns = Array.from(columns).sort((a, b) => {
            let indexA = Array.from(columns).indexOf(a);
            let indexB = Array.from(columns).indexOf(b);
            return colOrder[indexA] - colOrder[indexB];
        });
        tableRow.innerHTML = ""; // Remove content from the row
        sortedColumns.forEach((column) => {
            tableRow.append(column); // Add content to the row from the sorted array
        });
    });
}

// Following function will add row to the html table 
function addRows(){ 
    let table = document.getElementById('TemplateTable');
    let rowCount = table.rows.length; // Get total records of the table
    let cellCount = table.rows[0].cells.length; // Get number of columns from the table
    let row = table.insertRow(rowCount); // Add a new row to the table

    for(let i = 0; i < cellCount; i++){
        cell = row.insertCell(i); // Add each cell to the newly added row
        cell.className = "align-middle";
        cell.innerHTML = table.rows[1].cells[i].innerHTML.replaceAll("_0", "_"+(rowCount-1)); // Copy the HTML content of the cell from the 1st row
    }        

    try {
        // Set the newly added field disabled and copy their values from the 1st row
        try {
            let fieldId = "service_provider_name_" + (rowCount-1);
            document.getElementById(fieldId).disabled = true;
            document.getElementById(fieldId).value = document.getElementById("service_provider_name_0").value;
        } catch (error) {
            console.log("Error while disabling service provider " + error.message);
        }

        // Set the newly added field disabled and copy their values from the 1st row
        try {
            let fieldId = "source_geography_" + (rowCount-1);
            document.getElementById(fieldId).disabled = true;
            document.getElementById(fieldId).value = document.getElementById("source_geography_0").value;
        } catch (error) {
            console.log("Error while disabling source geography " + error.message);
        }

        try {
            let fieldId = "destination_geography_" + (rowCount-1);
            document.getElementById(fieldId).disabled = true;
            document.getElementById(fieldId).value = document.getElementById("destination_geography_0").value;
        } catch (error) {
            console.log("Error while disabling destination geography " + error.message);
        }

        try {
            let fieldId = "source_region_" + (rowCount-1);
            document.getElementById(fieldId).disabled = true;
            document.getElementById(fieldId).value = document.getElementById("source_region_0").value;
        } catch (error) {
            console.log("Error while disabling source region " + error.message);
        }

        try {
            let fieldId = "destination_region_" + (rowCount-1);
            document.getElementById(fieldId).disabled = true;
            document.getElementById(fieldId).value = document.getElementById("destination_region_0").value;
        } catch (error) {
            console.log("Error while disabling destination region " + error.message);
        }

        if (document.getElementById("weight_break_profile_0")) {
            try {
                let fieldId = "weight_break_profile_" + (rowCount-1);
                document.getElementById(fieldId).disabled = true;
                document.getElementById(fieldId).value = document.getElementById("weight_break_profile_0").value;
            } catch (error) {
                console.log("Error while disabling weight break profile " + error.message);
                console.log("This might be because weight break profile is not applicable for current offering");
            }
        }
        

        if (document.getElementById("charges_0")) {
            try {
                let chargesFieldName = "charges_" + (rowCount-1);
                document.getElementsByName(chargesFieldName).forEach((field, index) => { 
                    field.disabled = true;
                    document.getElementsByName("charges_0").forEach((field_0, index_0) => {
                        if (index == index_0)
                            field.checked = field_0.checked;
                    })
                });
            } catch (error) {
                console.log("Error while disabling charges " + error.message);
            }
        }

        // Enable existing contract checkbox in new row
        if (document.getElementById("existing_contract_0")) {
            try {
                let fieldId = "existing_contract_" + (rowCount-1);
                if (document.getElementById(fieldId))
                    document.getElementById(fieldId).disabled = false;
            } catch (error) {
                console.log("Error while enabling existing contract checkbox " + error.message);
            }
        }

        // Reset hidden field for existing contract checkbox
        if (document.getElementById("existing_contract_0")){
            try {
                {
                    document.getElementsByName("existing_contract_" + (rowCount-1)).forEach((field) => {
                        field.value = "N";
                    });
                }
            } catch (error) {
                console.log("Error while resetting existing contract hidden field " + error.message);
            }
        }
    } catch(e){  
        console.log("addRows 1st block " + e.message)  
    }

    try {
        // Add event handler to the service provider field of the 1st row so that it's values are replicated in subsequent rows
        try {
            document.getElementById("service_provider_name_0").addEventListener("change", function() {
                let table = document.getElementById('TemplateTable');
                let rowCount = table.rows.length;
                for (let i = 1; i < rowCount; i++) {
                    try {
                        document.getElementById("service_provider_name_" + i).value = document.getElementById("service_provider_name_0").value;
                    } catch(e){  
                        break;  
                    } 
                }
            });
        } catch (error) {
            console.log("Error while adding handler to source geography " + error.message);
        }

        // Add event handler to the source geography field of the 1st row so that it's values are replicated in subsequent rows
        try {
            document.getElementById("source_geography_0").addEventListener("change", function() {
                let table = document.getElementById('TemplateTable');
                let rowCount = table.rows.length;
                for (let i = 1; i < rowCount; i++) {
                    try {
                        document.getElementById("source_geography_" + i).value = document.getElementById("source_geography_0").value;
                    } catch(e){  
                        break;  
                    } 
                }
            });
        } catch (error) {
            console.log("Error while adding handler to source geography " + error.message);
        }

        // Add event handler to the destination geography field of the 1st row so that it's values are replicated in subsequent rows
        try {
            document.getElementById("destination_geography_0").addEventListener("change", function() {
                let table = document.getElementById('TemplateTable');
                let rowCount = table.rows.length;
                for (let i = 1; i < rowCount; i++) {
                    try {
                        document.getElementById("destination_geography_" + i).value = document.getElementById("destination_geography_0").value;
                    } catch(e){  
                        break;  
                    } 
                }
            });
        } catch (error) {
            console.log("Error while adding handler to destination geography " + error.message);
        }

        // Add event handler to the source region field of the 1st row so that it's values are replicated in subsequent rows
        try {
            document.getElementById("source_region_0").addEventListener("change", function() {
                let table = document.getElementById('TemplateTable');
                let rowCount = table.rows.length;
                for (let i = 1; i < rowCount; i++) {
                    try {
                        document.getElementById("source_region_" + i).value = document.getElementById("source_region_0").value;
                    } catch(e){  
                        break;  
                    } 
                }
            });
        } catch (error) {
            console.log("Error while adding handler to source region " + error.message);
        }

        // Add event handler to the destination region field of the 1st row so that it's values are replicated in subsequent rows
        try {
            document.getElementById("destination_region_0").addEventListener("change", function() {
                let table = document.getElementById('TemplateTable');
                let rowCount = table.rows.length;
                for (let i = 1; i < rowCount; i++) {
                    try {
                        document.getElementById("destination_region_" + i).value = document.getElementById("destination_region_0").value;
                    } catch(e){  
                        break;  
                    } 
                }
            });
        } catch (error) {
            console.log("Error while adding handler to destination regio " + error.message);
        }

        // Add event handler to the destination region field of the 1st row so that it's values are replicated in subsequent rows
        if (document.getElementById("weight_break_profile_0")) {
            try {
                document.getElementById("weight_break_profile_0").addEventListener("change", function() {
                    let table = document.getElementById('TemplateTable');
                    let rowCount = table.rows.length;
                    for (let i = 1; i < rowCount; i++) {
                        try {
                            document.getElementById("weight_break_profile_" + i).value = document.getElementById("weight_break_profile_0").value;
                        } catch(e){  
                            break;  
                        } 
                    }
                });
            } catch (error) {
                console.log("Error while adding handler to weight break profile " + error.message);
            }
        }        

        // Add event handler to the charges fields of the 1st row so that their values are replicated in subsequent rows
        if (document.getElementsByName("charges_0")) {
            try {
                document.getElementsByName("charges_0").forEach((field, index) => {
                    field.addEventListener("change", function() {
                    let table = document.getElementById('TemplateTable');
                    let rowCount = table.rows.length;
                    for (let i = 1; i < rowCount; i++) {
                        try {
                            document.getElementsByName("charges_" + i)[index].checked = document.getElementsByName("charges_0")[index].checked;
                        } catch(e){  
                            break;  
                        } 
                    }
                    });
                })
            } catch (error) {
                console.log("Error while adding handler to charges " + error.message);
            }
        }
    } catch(e){  
        console.log("addRows 2nd block " + e.message)  
    }

    try {
        // Keep existing contract and all its related fields disabled in the newly added row
        if (document.getElementById("existing_contract_0")) {
            document.getElementById("contract_name_" + (rowCount-1)).disabled = true;
            document.getElementById("start_date_" + (rowCount-1)).disabled = false;
            document.getElementById("end_date_" + (rowCount-1)).disabled = false;
        }        
    } catch(e){  
        console.log("addRows 3rd block " + e.message)   
    }
}

// Following function will delete the last row from the html table 
function deleteRows(){
    try {
        let table = document.getElementById('TemplateTable');
        let rowCount = table.rows.length;
        if(rowCount > 2){
            let row = table.deleteRow(rowCount-1);
            rowCount--;
        }
        else{
            alert('There should be atleast one row!');
        }
    } catch (error) {
        console.log("Error in deleteRows " + e.message);
    }
}

// Following function will enable/disable contract number, start date and end date fields based on the existing contract checkbox
function enableContractField(cb){
    try {
        let cbIndex = cb.id.replace("existing_contract_", "");
        let contractField = document.getElementById("contract_name_" + cbIndex);
        let startDateField = document.getElementById("start_date_" + cbIndex);
        let endDateField = document.getElementById("end_date_" + cbIndex);
    
        if (cb.checked) {
            // Enable Contract Number field
            contractField.disabled = false;
            startDateField.disabled = true;
            endDateField.disabled = true;
            startDateField.value = "";
            endDateField.value = "";
            document.getElementsByName(cb.id).forEach((field, index) => {
                field.value = "Y";
            });
        }
        else {
            contractField.disabled = true;
            contractField.selectedIndex = 0;
            startDateField.disabled = false;            
            endDateField.disabled = false;
            document.getElementsByName(cb.id).forEach((field, index) => {
                field.value = "N";
            });
        }
    } catch (e) {
        console.log("Error in enableContractField " + e.message);
    }
}

// Following function will populate contract number LOV based on the service provider using AJAX request 
function populateContractNumbers(serviceProviderField){
    try {
        let cbIndex = serviceProviderField.name.replace("service_provider_name_", "");
        let contractFieldId = "contract_name_" + cbIndex;
        var contractField = document.getElementById(contractFieldId);
        contractField.innerHTML = "";
        fetch(ajax_url_for_contracts, {
            method: "post",
            body: JSON.stringify({
                'service_provider': serviceProviderField.value,
            }),
            headers: {
                "X-CSRFToken": csrftoken,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then((response) => {
            return response.json();
        }).then((data) => {
            let html_data = '<option hidden disabled selected value> ---- </option>';
            Object.keys(data).forEach((key) => {
                record = data[key];
                id = record["id"];
                value = record["value"];
                html_data += `<option value="${id}">${value}</option>`;
            });
            contractField.innerHTML = html_data;
        }).catch((e) => {
            console.log("Error in populateContractNumbers - POST request failed - " + e.message);
        });

    } catch (e) {
        console.log("Error in populateContractNumbers " + e.message);
    }
}

// function populateRateTypes(offeringTypeField){
//     var rateTypeField = document.getElementById("rate_type");
//     rateTypeField.innerHTML = "";
//     // Invoke AJAX request to fetch list of contracts
//     fetch(ajax_url_for_rate_type, {
//         method: "post",
//         body: JSON.stringify({
//             'offering_type': offeringTypeField.value,
//         }),
//         headers: {
//             "X-CSRFToken": csrftoken,
//             'Accept': 'application/json',
//             'Content-Type': 'application/json'
//         }
//     }).then((response) => {
//         return response.json();
//     }).then((data) => {
//         console.log(data);
//         let html_data = '<option hidden disabled selected value> ---- </option>';
//         Object.keys(data).forEach((key) => {
//             record = data[key];
//             id = record["id"];
//             value = record["value"];
//             html_data += `<option value="${id}">${value}</option>`
//         });
//         rateTypeField.innerHTML = html_data;
//     }).catch((e) => {
//         console.log("Error in populateContractNumbers - POST request failed - " + e.message);
//     });
// }

function populateRateTypes(offeringTypeField){
    var rateTypeDiv = document.getElementById("rate_type_div");
    // Invoke AJAX request to fetch list of contracts
    fetch(ajax_url_for_rate_type, {
        method: "post",
        body: JSON.stringify({
            'offering_type_group_name': offeringTypeField.value
        }),
        headers: {
            "X-CSRFToken": csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log(data);
        let html_data = '';
        Object.keys(data).forEach((key, index) => {
            record = data[key];
            id = record["id"];
            value = record["value"];
            // html_data += 
            // `<input class="btn-check" type="radio" name="rate_type" id="rate_type_option_${index}" value="${id}" onchange="populateTemplateBatches(this)" required><label class="btn btn-outline-primary" for="rate_type_option_${index}">${value}</label>&nbsp;`
            html_data += 
            `<input class="btn-check" type="radio" name="rate_type" id="rate_type_option_${index}" value="${id}" required><label class="btn btn-outline-primary" for="rate_type_option_${index}">${value}</label>&nbsp;`
        });
        rateTypeDiv.innerHTML = html_data;

        setRateTypeFromSession(); // Now that all rate types have been included in this html, try to select one of them if template id is available in session
    }).catch((e) => {
        console.log("Error in populateContractNumbers - POST request failed - " + e.message);
    });
}

/*
function populateTemplateBatches(rateTypeField){
    var templateBatchField = document.getElementById("template_batch");
    templateBatchField.innerHTML = "";
    // Invoke AJAX request to fetch list of contracts
    fetch(ajax_url_for_template_batches, {
        method: "post",
        body: JSON.stringify({
            'template_id': rateTypeField.value,
        }),
        headers: {
            "X-CSRFToken": csrftoken,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log(data);
        let html_data = "";
        let templateFound = false;
        Object.keys(data).forEach((key) => {
            record = data[key];
            id = record["id"];
            value = record["value"];
            html_data += `<option value="${id}">${value}</option>`
            templateFound = true;
        });
        if (templateFound) {
            templateBatchField.innerHTML = "'<option hidden disabled selected value> --- Available Templates --- </option>'" + html_data;
        }
    }).catch((e) => {
        console.log("Error in populateContractNumbers - POST request failed - " + e.message);
    });
}
*/

// Following function will reset all fields in the form (all rows in the table) to their original states
function resetForm() {
    try {
        document.getElementById("template_form").reset();
        let table = document.getElementById('TemplateTable');
        let rowCount = table.rows.length;
        for (let i = 0; i < rowCount; i++) {
            try {
                // Reset contract name LOV
                document.getElementById("contract_name_" + i).selectedIndex = 0;
                if (document.getElementById("existing_contract_" + i)) {
                    // Enable existing contract checkbox
                    document.getElementById("existing_contract_" + i).disabled = false;
                    // Disable contract name LOV
                    document.getElementById("contract_name_" + i).disabled = true;
                    // Enable start date
                    document.getElementById("start_date_" + i).disabled = false;
                    // Enable end date
                    document.getElementById("end_date_" + i).disabled = false;
                    // Reset hidden field for existing contract checkbox
                    document.getElementsByName("existing_contract_" + i).forEach((field) => {
                        field.value = "N";
                    });
                }
            } catch(e){  
                break;  
            } 
        }
        // Disable template name field
        document.getElementById("template_name").disabled = true;
    } catch (e) {
        console.log("Error in resetForm " + e.message);
    }    
}

// Following function will clear only the geographical related fields
function clearGeographies() {
    try {
        // Disable all contract number, start date and end date fields and remove the content of the contract number field
        let table = document.getElementById('TemplateTable');
        let rowCount = table.rows.length;
        for (let i = 0; i < rowCount; i++) {
            try {
                document.getElementById("source_geography_" + i).selectedIndex = 0;
                document.getElementById("destination_geography_" + i).selectedIndex = 0;
                document.getElementById("source_region_" + i).selectedIndex = 0;
                document.getElementById("destination_region_" + i).selectedIndex = 0;
            } catch(e){  
                break;  
            } 
        }
        // Disable template name field
        document.getElementById("template_name").disabled = true;
    } catch (e) {
        console.log("Error in resetForm " + e.message);
    }    
}

// Following function will enable/disable template name field based on the save template checkbox
function enableTemplateNameField(cb) {
    try {
        if (cb.checked) {
            document.getElementById("template_name").disabled = false;         
        }
        else {
            document.getElementById("template_name").disabled = true;
            document.getElementById("template_name").value = "";
        }
    } catch (e) {
        console.log("Error in enableTemplateNameField " + e.message);
    }
}

// Following function will populate the html table from a saved template, this gets invoked after the page loads
function setValuesFromSavedTemplate(jsonString) {
    // jsonString parameter is a dictionary that contains field names and their values from a saved template
    // If that is blank, then it means no existing template was selected for reuse, don't do anything in that case
    if (jsonString.trim() == "")
        return;

    try {
        const obj = JSON.parse(jsonString);
        let tableRecordCount = obj["table_record_count"]; // Get how many records the html table should have
        tableRecordCount = Number(tableRecordCount);

        console.log("tableRecordCount = "+tableRecordCount);

        for (let i=1; i< tableRecordCount-1; i++) {
            addRows(); // Add those rows to the table
        }

        // For each element of the dictionary, set the value to the field. Key is the field name, Value is its content
        for (const [key, value] of Object.entries(obj)) {
            try {
                // Don't set default values to some fields, even if their valus exist in a saved template
                if (key == "save_template_cb")
                    console.log("Ignore field " + key);
                else if (key == "template_name")
                    console.log("Ignore field " + key);
                else if (key.startsWith("existing_contract_"))
                    console.log("Ignore field " + key);
                else if (key.startsWith("contract_name_"))
                    console.log("Ignore field " + key);
                // else if (key.startsWith("start_date_"))
                //     console.log("Ignore field " + key);
                // else if (key.startsWith("end_date_"))
                //     console.log("Ignore field " + key);
                else if (key.startsWith("charges_")) {
                    // Set default values to charges fields
                    let values = value.split("|")

                    document.getElementsByName("charges_0").forEach((field, index) => {
                        if (values.includes(field.value))
                            field.checked = true;
                    });
                } 
                else {
                    // Set default values to the remaining fields
                    document.getElementById(key).value = value;

                    // While populating default values to the service provider fields, 
                    // invoke the AJAX request so that the contract number LOV can remain populated at the background
                    if (key.startsWith("service_provider_name_")) {
                        populateContractNumbers(document.getElementById(key));
                    }
                }                  
            } catch(e){  
                console.log("setValuesFromSavedTemplate - unable to set default value to a field - " + key + " - " + value)  
            }
        }

        let table = document.getElementById('TemplateTable');
        let rowCount = table.rows.length;

        // Copy the content of the service provider from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("service_provider_name_" + i).value = document.getElementById("service_provider_name_0").value;
            } catch(e){  
                break;  
            } 
        }

        // Copy the content of the source geography from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("source_geography_" + i).value = document.getElementById("source_geography_0").value;
            } catch(e){  
                break;  
            } 
        }
        // Copy the content of the destination geography from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("destination_geography_" + i).value = document.getElementById("destination_geography_0").value;
            } catch(e){  
                break;  
            } 
        }
        // Copy the content of the source region from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("source_region_" + i).value = document.getElementById("source_region_0").value;
            } catch(e){  
                break;  
            } 
        }
        // Copy the content of the destination region from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("destination_region_" + i).value = document.getElementById("destination_region_0").value;
            } catch(e){  
                break;  
            } 
        }
        // Copy the content of the weight break profile from the 1st row to the subsequent rows
        for (let i = 1; i < rowCount; i++) {
            try {
                document.getElementById("weight_break_profile_" + i).value = document.getElementById("weight_break_profile_0").value;
            } catch(e){  
                break;  
            } 
        }
        // Copy the content of the charges fields from the 1st row to the subsequent rows
        document.getElementsByName("charges_0").forEach((field, index) => {
            for (let i = 1; i < rowCount; i++) {
                try {
                    document.getElementsByName("charges_" + i)[index].checked = document.getElementsByName("charges_0")[index].checked;
                } catch(e){  
                    break;  
                } 
            }
        })
        // Set focus to Download Excel Template button
        document.getElementById("submit_button").focus();
    }
    catch(e){  
        console.log("Error in setValuesFromSavedTemplate " + e.message);
    }   
}

// This function will perform all the validations
function validate() {
    document.getElementById("validation_message").innerText = ""
    ready = true;
    // Check if record count fields are filled in all rows
    const recordCountElements = document.querySelectorAll('*[id^="excel_row_count_"]');
    recordCountElements.forEach((recordCountElement) => {
        if (recordCountElement.value == "") {
            recordCountElement.style.borderColor = "red";
            recordCountElement.style.borderWidth = 2;
            ready = false;
            document.getElementById("validation_message").innerText = "Record Count must be provided."
            //document.getElementById("validation_message_parent").style.visibility='visible';
            document.getElementById("validation_message_parent").style.opacity = 1;
        }
        else{
            recordCountElement.style.removeProperty("border");
        }
    });

    // Check if service provider has been provided
    if (ready) {
        if (document.getElementById("service_provider_name_0")) {
            const fields = document.querySelectorAll('*[id^="service_provider_name_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Service Provider must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    if (ready) {
        // Check if source geography or source region is selected
        if((document.getElementById("source_geography_0").selectedIndex == 0) && (document.getElementById("source_region_0").selectedIndex == 0)) {
            ready = false;
            document.getElementById("validation_message").innerText = "Select Source Geography or Source Region."
            //document.getElementById("validation_message_parent").style.visibility='visible';
            document.getElementById("validation_message_parent").style.opacity = 1;
            document.getElementById("source_geography_0").style.borderColor = "red";
            document.getElementById("source_region_0").style.borderColor = "red";
            document.getElementById("source_geography_0").style.borderWidth = 2;
            document.getElementById("source_region_0").style.borderWidth = 2;
        }
        else {
            document.getElementById("source_geography_0").style.removeProperty("border");
            document.getElementById("source_region_0").style.removeProperty("border");
        }
    }

    if (ready) {
        // Check if both source geography and source region are selected
        if((document.getElementById("source_geography_0").selectedIndex != 0) && (document.getElementById("source_region_0").selectedIndex != 0)) {
            document.getElementById("source_geography_0").selectedIndex = 0;
            document.getElementById("source_region_0").selectedIndex = 0;
            let table = document.getElementById('TemplateTable');
            let rowCount = table.rows.length;
            for (let i = 1; i < rowCount; i++) {
                try {
                    document.getElementById("source_geography_" + i).value = document.getElementById("source_geography_0").value;
                    document.getElementById("source_region_" + i).value = document.getElementById("source_region_0").value;
                } catch(e){  
                    break;  
                } 
            }
            ready = false;
            document.getElementById("validation_message").innerText = "Both Source Geography and Source Region should not be selected at the same time."
            //document.getElementById("validation_message_parent").style.visibility='visible';
            document.getElementById("validation_message_parent").style.opacity = 1;
            document.getElementById("source_geography_0").style.borderColor = "red";
            document.getElementById("source_region_0").style.borderColor = "red";
            document.getElementById("source_geography_0").style.borderWidth = 2;
            document.getElementById("source_region_0").style.borderWidth = 2;
        }
        else {
            document.getElementById("source_geography_0").style.removeProperty("border");
            document.getElementById("source_region_0").style.removeProperty("border");
        }
    }

    if (ready) {
        // Check if  destination geography or destination region is selected
        if((document.getElementById("destination_geography_0").selectedIndex == 0) && (document.getElementById("destination_region_0").selectedIndex == 0)) {
            ready = false;
            document.getElementById("validation_message").innerText = "Select Destination Geography or Destination Region."
            //document.getElementById("validation_message_parent").style.visibility='visible';
            document.getElementById("validation_message_parent").style.opacity = 1;
            document.getElementById("destination_geography_0").style.borderColor = "red";
            document.getElementById("destination_region_0").style.borderColor = "red";
            document.getElementById("destination_geography_0").style.borderWidth = 2;
            document.getElementById("destination_region_0").style.borderWidth = 2;
        }
        else {
            document.getElementById("destination_geography_0").style.removeProperty("border");
            document.getElementById("destination_region_0").style.removeProperty("border");
        }
    }    

    if (ready) {
        // Check if both destination geography and destination region are selected
        if((document.getElementById("destination_geography_0").selectedIndex != 0) && (document.getElementById("destination_region_0").selectedIndex != 0)) {
            document.getElementById("destination_geography_0").selectedIndex = 0;
            document.getElementById("destination_region_0").selectedIndex = 0;
            let table = document.getElementById('TemplateTable');
            let rowCount = table.rows.length;
            for (let i = 1; i < rowCount; i++) {
                try {
                    document.getElementById("destination_geography_" + i).value = document.getElementById("destination_geography_0").value;
                    document.getElementById("destination_region_" + i).value = document.getElementById("destination_region_0").value;
                } catch(e){  
                    break;  
                } 
            }
            ready = false;
            document.getElementById("validation_message").innerText = "Both Destination Geography and Destination Region should not be selected at the same time."
            //document.getElementById("validation_message_parent").style.visibility='visible';
            document.getElementById("validation_message_parent").style.opacity = 1;
            document.getElementById("destination_geography_0").style.borderColor = "red";
            document.getElementById("destination_region_0").style.borderColor = "red";
            document.getElementById("destination_geography_0").style.borderWidth = 2;
            document.getElementById("destination_region_0").style.borderWidth = 2;
        }
        else {
            document.getElementById("destination_geography_0").style.removeProperty("border");
            document.getElementById("destination_region_0").style.removeProperty("border");
        }
    }

    // Check if equipment has been provided
    if (ready) {
        if (document.getElementById("equipment_0")) {
            const fields = document.querySelectorAll('*[id^="equipment_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Equipment must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if currency has been provided
    if (ready) {
        if (document.getElementById("currency_0")) {
            const fields = document.querySelectorAll('*[id^="currency_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Currency must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if weight uom has been provided
    if (ready) {
        if (document.getElementById("weight_uom_0")) {
            const fields = document.querySelectorAll('*[id^="weight_uom_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Weight UOM must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if volume uom has been provided
    if (ready) {
        if (document.getElementById("volume_uom_0")) {
            const fields = document.querySelectorAll('*[id^="volume_uom_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Volume UOM must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if weight break profile has been provided
    if (ready) {
        if (document.getElementById("weight_break_profile_0")) {
            const fields = document.querySelectorAll('*[id^="weight_break_profile_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Volume UOM must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if contract name has been provided when rate type is Discount
    if (ready) {
        if (rate_type_name.toUpperCase() == "DISCOUNT") {
            const fields = document.querySelectorAll('*[id^="contract_name_"]');
            fields.forEach((field) => {
                if (field.value == "") {
                    ready = false;
                    document.getElementById("validation_message").innerText = "Contract must be selected."
                    //document.getElementById("validation_message_parent").style.visibility='visible';
                    document.getElementById("validation_message_parent").style.opacity = 1;
                    field.style.borderColor = "red";
                    field.style.borderWidth = 2;
                }
                else {
                    field.style.removeProperty("border");
                }
            });
        }
    }

    // Check if contract name has been provided when existing checbox is checked
    if (ready) {
        if (document.getElementById("existing_contract_0")) {
            let table = document.getElementById('TemplateTable');
            let rowCount = table.rows.length;
            for (let i = 0; i < rowCount-1; i++) {
                try {
                    if ((document.getElementById("existing_contract_" + i).checked) && (document.getElementById("contract_name_" + i).value == "")) {
                        ready = false;
                        document.getElementById("validation_message").innerText = "If Existing Contract is selected then contract name must be provided."
                        //document.getElementById("validation_message_parent").style.visibility='visible';
                        document.getElementById("validation_message_parent").style.opacity = 1;
                        document.getElementById("contract_name_" + i).style.borderColor = "red";
                        document.getElementById("contract_name_" + i).style.borderWidth = 2;
                    }
                    else {
                        document.getElementById("contract_name_" + i).style.removeProperty("border");
                    }
                } catch(e){  
                    console.log("Error in existing contract validation " + e.message)
                } 
            }
        }
    }
    
    if (ready){
        document.getElementById("validation_message_parent").style.opacity = 0;
        if (document.getElementById("save_template_cb").checked) {
            document.getElementById("popupModalBody").innerText = "Entered details have been saved for future use. Generating Excel Template for download...";
        }
        else {
            document.getElementById("popupModalBody").innerText = "Generating Excel Template for download...";
        }
        document.getElementById("modal_button").click(); // This will show modal and will invoke initiateSubmit
    }
    // else {
    //     setTimeout(() => {
    //         var fadeTarget = document.getElementById("validation_message_parent");
    //         var fadeEffect = setInterval(function () {
    //             if (!fadeTarget.style.opacity) {
    //                 fadeTarget.style.opacity = 1;
    //             }
    //             if (fadeTarget.style.opacity > 0) {
    //                 fadeTarget.style.opacity -= 0.4;
    //             } else {
    //                 clearInterval(fadeEffect);
    //             }
    //         }, 200);
    //     }, 5000);        
    // }
}

// Following function will store the table row count in hidden field and will initiate submit
function initiateSubmit() {
    try {
        let table = document.getElementById('TemplateTable');
        let rowCount = table.rows.length;
        document.getElementById("table_record_count").value = rowCount;

        setTimeout("submitForm()", 3000); // set timout 
    }
    catch(e){  
        console.log("Error in populateTableRecordsCount " + e.message);
    }
}

// This will close the modal and will submit the form
function submitForm() {
    document.querySelector('#close-button').click();
    document.getElementById("template_form").submit();
}

// Following function will render the HTML table, will be invoked from onload event of the body
function renderPage(jsonString) {
    setValuesFromSavedTemplate(jsonString);
    rearrangeTableColumns();
}

// Following function will populate rate types for the selected offering
function invokePopulateRateType() {
    try {
        offeringTypes = document.querySelectorAll("[id^='offering_']"); // Get all offering fields
        offeringTypes.forEach(element => {
            try {
                if(element.checked) {
                    populateRateTypes(element); // If the offering is selected, then populate rate types for that offering
                }
            } catch (error) {
                
            }
        });
    }
    catch (e) {
        console.log("Error while invoking populateRateTypes " + e.message);
    }
}

// Following function will select the rate type based on the template id stored in session
function setRateTypeFromSession() {
    try {
        rateTypes = document.querySelectorAll("[id^='rate_type_option_']");
        rateTypes.forEach(element => {
            try {
                if(element.value == templateId) {
                    element.checked = true;
                    //populateTemplateBatches(element)
                }
            } catch (error) {
                
            }
        });
    }
    catch (e) {
        console.log("Error in setRateTypeFromSession while invoking populateRateTypes " + e.message);
    }
}