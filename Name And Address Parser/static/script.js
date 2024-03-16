/* function openTab(tabName, event) {
    var i;
    var tabContents = document.getElementsByClassName("tabcontent");
    var tabLinks = document.getElementsByClassName("tablink");

    for (i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none"; // Hide all tab content
    }

    for (i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" active", ""); // Remove "active" class from all tabs
    }

    document.getElementById(tabName).style.display = "block"; // Show the content of the clicked tab
    event.currentTarget.className += " active"; // Add "active" class to the clicked tab
}
document.getElementById('defaultOpen').click();
*/

//------------------------------------------------------------------------------------------------------------
//                                 Single Line Address Parser Tab Functionality
//------------------------------------------------------------------------------------------------------------

$(document).ready(function () {
    
    isExceptionForced = false;

    $('#mapdata').hide();
    $('#result-box').hide()
    $('#myForm').submit(function (event) {
        event.preventDefault();
        $('#result-box').show();
        var addressValue = $('#address-input').val();
        $.ajax({
            type: "POST",
            url: "/",
            data: { address: addressValue },
            success: function (response) {
                console.log('Response:', response);
                renderAddressData(response);
                document.getElementById('exception-controls').style.display = 'block';
                isExceptionForced = false;
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    $('#exception-checkbox').change(function() {
        // Check if the checkbox is checked
        if ($(this).is(':checked')) {
            // Enable the button if checkbox is checked
            $('#exception-btn').prop('disabled', false);
        } else {
            // Disable the button if checkbox is unchecked
            $('#exception-btn').prop('disabled', true);
            
        }
    });


    // Event listener for the exception button
    $('#exception-btn').on('click', function () {
        // var forceException = $('#exception-checkbox').is(':checked');
        if (isExceptionForced) {
            alert("Exception already created for this address.");
        } else {
            var unsatisfied_address = $('#address-input').val();
            
            // AJAX request to the server with the forceException value
            $.ajax({
                type: "POST",
                url: "/forceException",
                data: { address: unsatisfied_address },
                success: function (response) {
                    console.log("Response:", response);
                    isExceptionForced = true;
                    alert("Forced Exception is Created!");
                },
                error: function (error) {
                    console.error("Error:", error);
                }
            });
        }
    });
    var parsedByInfo = $('<div id="parsed-by-info" style="display: flex; justify-content: center; align-items: center; margin-top: 10px;"></div>');
    $('#exception-controls').after(parsedByInfo);
    

    function renderAddressData(data) {
        var tableBody = $('#resultBody');
        tableBody.empty();
        var tableHTML = '';

        if (data && data.result && data.result.Output && data.result.Parsed_By) {
            var addressComponents = data.result.Output;
            var parsedBy = data.result.Parsed_By;
            $('#parsed-by-info').text('Address Parsed By --> ' + parsedBy);
            addressComponents.forEach(function (array, index) {

                tableHTML += '<tr>';
                tableHTML += '<td>' + array[2] + '</td>'; // Token
                tableHTML += '<td>' + array[0] + '</td>'; // Address
                tableHTML += '<td>' + array[1] + '</td>'; // Component
                tableHTML += '<td>' + array[3] + '</td>'; // Component Description
                //tableHTML += '<td>' + parsedBy + '</td>'; // Parsed By
                // if (index === 0) {
                //     tableHTML += '<td rowspan="' + addressComponents.length + '" style="vertical-align: top;">' + parsedBy + '</td>';
                // }
                tableHTML += '</tr>';
                // tableHTML += wrapTableData(array);
            });

            tableBody.html(tableHTML);
            $('#resultTable').show();
            $('#resultTable thead').show();
        } else {
            console.error('Data structure issue: Output is undefined.');
            $('#resultTable').hide();
            $('#resultTable thead').hide();
        }
    }
});

//------------------------------------------------------------------------------------------------------------
//                     Batch Parser Tab Functionality
//------------------------------------------------------------------------------------------------------------

$(document).ready(function () {
    $('#BatchForm').submit(function (event) {
        event.preventDefault(); // Prevent default form submission

        var fileData = new FormData(this);
        fileData.append('file', $('#file-upload')[0].files[0]);

        $.ajax({
            url: '/Batch_Parser',
            type: 'POST',
            data: fileData,
            contentType: false,
            processData: false,
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        var percentComplete = (e.loaded / e.total) * 100;
                        // Update your front-end progress bar here
                    }
                }, false);
                return xhr;
            },
            // Inside the success callback of your $.ajax request
            success: function (response) {
                console.log('File uploaded!');

                // Replace newlines with <br> tags and tabs with four non-breaking spaces
                var formattedText = response.metrics.metrics.replace(/\n/g, '<br>').replace(/\t/g, '&nbsp;&nbsp;&nbsp;&nbsp;');

                // Set the formatted text to your metrics display element
                document.getElementById('metrics-display').innerHTML = formattedText;

                // Show the metrics box
                document.getElementById('metrics-display').style.display = 'block';
            },

            error: function (error) {
                console.log('Upload error:', error);
            }
        });
    });
});


//------------------------------------------------------------------------------------------------------------
//                                  Map Creation Form Tab Functionality
//------------------------------------------------------------------------------------------------------------      

let data = [];
let currentKeyIndex = 0;

document.getElementById("loadFileBtn").addEventListener("click", loadFile);
document.getElementById("submit&NextBtn").addEventListener("click", showNext);
document.getElementById("clear&exitBtn").addEventListener("click", exitFunction);


function loadFile() {
    let container = document.getElementById("mapdata");
    if (container) {
        container.style.display = 'grid'; // Adjust the display style as per your original layout
    } else {
        console.error("Container element not found");
        return; // Exit the function if the container is not found
    }

    const jsonFileInput = document.getElementById("jsonFileInput");

    if (jsonFileInput.files.length > 0) {
        const file = jsonFileInput.files[0];
        const filenameElement = document.getElementById("filename");
        if (filenameElement) {
            filenameElement.value = file.name;
        } else {
            console.error("filename element not found");
        }

        const reader = new FileReader();

        reader.onload = function (e) {
            try {
                const newData = JSON.parse(e.target.result);
                data = newData; // Append new data to existing data array
                if (data.length > 1) {
                    document.getElementById("submit&NextBtn").style.display = 'block';
                    document.getElementById("submitBtn").style.display = 'none';
                } else {
                    document.getElementById("submit&NextBtn").style.display = 'none';
                    document.getElementById("submitBtn").style.display = 'block';
                }
                currentKeyIndex = 0;
                showNext(); // Start processing data if it's the first file

            } catch (error) {
                console.error("Parsing error:", error);
                alert("Invalid JSON data. Please provide a valid JSON file.", error.message);
            }
        };

        reader.readAsText(file);
    } else {
        alert("Please select a JSON file.");
    }

}

function showNext() {
    if (currentKeyIndex < data.length) {
        const currentData = data[currentKeyIndex];
        const keys = Object.keys(currentData);
        document.getElementById("recordId").value = currentData["Record ID"];
        document.getElementById("inputValue").value = currentData["INPUT"];
        document.getElementById("mask-inputValue").value = keys[2];

        const otherDataKey = findThirdObjectKey(currentData);
        const otherData = currentData[otherDataKey];
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = "";
        fetchOptionsAndPopulateDropdowns(otherData, otherDataKey);

        updateDictionaryDisplay();
        $.ajax({
            type: "POST",
            url: "/update_dictionary", // Adjust the URL as needed
            contentType: "application/json",
            data: JSON.stringify({ index: currentKeyIndex }),
            success: function(response) {
                // The dictionary has been removed from the server, move to the next one
                console.log(response);
                if (currentKeyIndex < data.length - 1) {
                    currentKeyIndex++;
                    showNext();
                } else {
                    alert("End of data reached");
                    // Perform any cleanup if needed
                }
            },
            error: function(error) {
                console.error("Failed to remove the dictionary on the server:", error);
            }
        });
    } else {
        alert("End of data reached");
        currentKeyIndex = data.length;
    }

}



function updateDictionaryDisplay() {
    const totalDictionaries = data.length;
    const currentDictionaryIndex = totalDictionaries > 0 ? currentKeyIndex + 1 : 0;
    document.getElementById("currentDictionaryDisplay").textContent = `${currentDictionaryIndex}/${totalDictionaries}`;
}

function fetchOptionsAndPopulateDropdowns(otherData, otherDataKey) {
    fetch("/AddressComponents_dropdown")
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(options => {
            populateDropdowns(otherData, otherDataKey, options);
        })
        .catch(error => console.error('Error fetching options:', error));
}

function handleNextDictionary() {
    if (currentKeyIndex < data.length) {
        data.splice(currentKeyIndex, 1); // Remove the processed dictionary

        // Update the dictionary display
        updateDictionaryDisplay();

        if (data.length > 0) {
            // Do not automatically call showNext here. It will be called after user actions.
        } else {
            alert("All Dictionaries Processed");
        }
    }
}

function populateDropdowns(otherData, otherDataKey, options) {
    const tableBody = document.getElementById("table-body");
    console.log("populateDropdowns called with data", otherData);
    
    if (otherDataKey) {
        otherData.forEach(function (item) {
            const row = document.createElement("tr");
            tableBody.appendChild(row);
            const reorderedItem = [item[2], item[0], item[3]];
            reorderedItem.forEach(function (value, index) {
                //const value = item[index];
                const td = document.createElement("td");
                if (index == 2) {
                    // Convert value column to a dropdown menu
                    const valueSelect = document.createElement("select");
                    valueSelect.name = "value";
                    //const options = ["USAD_SNO", "USAD_SNM", "USAD_SFX", "USAD_ANO", "USAD_ANM", "USAD_CTY", "USAD_STA", "USAD_ZIP", "USAD_SPR", "USAD_BNM", "USAD_BNO", "USAD_SPT", "USAD_ZP4", "USAD_RNM", "USAD_RNO", "USAD_ORG", "USAD_MGN", "USAD_MDG", "USAD_HNO", "USAD_HNM", "USAD_NA"];
                    options.forEach(function (optionValue) {
                        const optionElement = document.createElement("option");
                        optionElement.value = optionValue;
                        optionElement.textContent = optionValue;
                        valueSelect.appendChild(optionElement);
                    });
                    valueSelect.value = value;
                    td.appendChild(valueSelect);
                } else {
                    td.textContent = value;
                }
                row.appendChild(td);
            });
        });
        currentKeyIndex++;
        
    } else {
        alert("No third object found in the current data.");
    }
    console.log("Finished populating table");
}

function exitFunction() {
    // Hide the container instead of removing it
    const container = document.getElementById("mapdata");
    if (container) {
        container.style.display = "none"; // Hide the container
    }

    // Reset the file input
    const fileInput = document.getElementById("jsonFileInput");
    if (fileInput) {
        fileInput.value = "";
    }
}

function findThirdObjectKey(data) {
    for (const key in data) {
        if (key !== "Record ID" && key !== "INPUT") {
            return key;
        }
    }
    return null; // No third object key found
}


//-----------------------------------------------------------------------------
//                      "Collect and Push Map Creation Form data to Server"
//-----------------------------------------------------------------------------

function collectData() {
    // Example: Collect data from input fields
    console.log("collectData called");
    const record_Id = document.getElementById("recordId").value;
    const file_name = document.getElementById("filename").value;
    const input_Value = document.getElementById("inputValue").value;
    const mask = document.getElementById("mask-inputValue").value;
    const address_region = document.getElementById("region") ? document.getElementById("region").value : null;
    const Address_Type = document.getElementById("AddressType") ? document.getElementById("AddressType").value : null;
    const approval = document.getElementById("Approved?") ? document.getElementById("Approved?").value : null;
    const approved_by = document.getElementById("approvedby") ? document.getElementById("approvedby").value : null;


    // Example: Collect data from table
    const mappingData = [];
    const tbody = document.getElementById("table-body");
    if (!tbody) {
        console.error("Tbody element with ID 'table-body' not found.");
        return; // Exit the function if the tbody isn't found
    }
    const rows = tbody.getElementsByTagName("tr");
    console.log("Rows: ", rows);
    const dicData = {};
    for (let i = 0; i < rows.length; i++) {
        const cells = rows[i].getElementsByTagName("td");
        console.log(`Row ${i} cells:`, cells);
        if (cells.length < 3) {
            console.error(`Row ${i} is missing one or more cells.`);
            continue;
        }
        const rowData = {
            "Mask Token": cells[0].textContent,
            "Address Token": cells[1].textContent,
        };
        rowData["Address Component"] = cells[2].querySelector("select")
        ? cells[2].querySelector("select").value
        : cells[2].textContent;
        dicData[i+1] = rowData["Address Component"]
        mappingData.push(rowData);
    }
    console.log("Data collected", mappingData);
    result = {
        "Record Id": record_Id,
        "Exception_File_Name": file_name,
        "Input": input_Value,
        "Mask Pattern": mask,
        "Region": address_region,
        "Type": Address_Type,
        "Address Approved?": approval,
        "Approved By": approved_by,
        "Mapping Data": mappingData
    };
    result[mask] = dicData;
    return result;

}


// document.getElementById("submitBtn").addEventListener("click", function () {
//     const approved = document.getElementById("Approved?").value;
//     if (approved === "Yes" && validateDropdowns()) {
//         const data = collectData();
//         checkForExistingMask(data["Mask Pattern"], data);
//     } else if (approved === "No") {
//         // If approved is "No", skip to the next dictionary
//         handleNextDictionary();
//     } else {
//         alert("Please fill in all required fields.");
//     }
// });

// document.getElementById("submit&NextBtn").addEventListener("click", function () {
//     const approved = document.getElementById("Approved?").value;
//     if (approved === "Yes" && validateDropdowns()) {
//         const data = collectData();
//         checkForExistingMask(data["Mask Pattern"], data);
//     } else if (approved === "No") {
//         // If approved is "No", skip to the next dictionary
//         handleNextDictionary();
//     } else {
//         alert("Please fill in all required fields.");
//     }
// });

document.getElementById("submitBtn").addEventListener("click", function () {
    setTimeout(() => {
        submitButtonHandler();
    }, 3000); // Wait for 3 seconds before handling the submission
});

document.getElementById("submit&NextBtn").addEventListener("click", function () {
    setTimeout(() => {
        submitButtonHandler();
    }, 3000); // Wait for 3 seconds before handling the submission
});

function submitButtonHandler() {
    const approved = document.getElementById("Approved?").value;
    if (approved === "Yes" && validateDropdowns()) {
        const data = collectData();
        checkForExistingMask(data["Mask Pattern"], data);
    } else if (approved === "No") {
        // If approved is "No", skip to the next dictionary
        handleNextDictionary();
    } else {
        alert("Please fill in all required fields.");
    }
}



function validateDropdowns() {
    // Helper function to check if element exists and its value is not empty
    function isDropdownValid(id) {
        const element = document.getElementById(id);
        return element.value !== "" && element.value !== "Not Selected";
    }

    // Check each dropdown
    if (!isDropdownValid("region")) return false;
    if (!isDropdownValid("AddressType")) return false;
    if (!isDropdownValid("Approved?")) return false;
    if (!isDropdownValid("approvedby")) return false;

    // Check each address component dropdown
    const dropdowns = document.querySelectorAll("select[name='value']");
    for (let i = 0; i < dropdowns.length; i++) {
        if (dropdowns[i].value === "Not Selected") {
            return false;
        }
    }
    return true;
}



function checkForExistingMask(mask, data) {
    $.ajax({
        type: "POST",
        url: "/check-mask-existence",
        contentType: "application/json",
        data: JSON.stringify({ mask: mask }),
        success: function (response) {
            if (response.exists) {
                if (confirm("Mask found in KnowledgeBase, do you want to overwrite the existing entry?")) {
                    sendDataToServer(data);
                } else {
                    // Move to the next address or perform other actions as needed
                }
            } else {
                sendDataToServer(data);
            }
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // Handle errors
        }
    });
}



function sendDataToServer(data) {
    $.ajax({
        type: "POST",
        url: "/MapCreationForm-Data",
        contentType: "application/json",
        data: JSON.stringify(data),
        success: function (response) {
            console.log("Success:", response);
            alert("Mapping Created and sent to Knowledgebase");
            if (currentKeyIndex < data.length) {
                data.splice(currentKeyIndex, 1);

                // Update the dictionary display
                handleNextDictionary();
            }
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
            // Handle errors
        }
    });
}







//------------------------------------------------------------------------------------------------------------
//                                  User Defined Components Tab Functionality
//------------------------------------------------------------------------------------------------------------

function fetchComponentData() {
    $.ajax({
        type: "POST",
        url: "/UserDefinedComponents",
        success: function (response) {
            console.log('Response:', response);
            populateComponentsTable(response.result);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}
$('#userdfc').click(function(){
    $('#fetchall').click();
    $('#fetchall').hide();
});

function populateComponentsTable(components) {
    var tableBody = $('#udresultBody');
    tableBody.empty(); // Clear existing table rows
    var tableHTML = '';

    // Loop through the received JSON data
    for (var key in components) {
        tableHTML += '<tr>';
        tableHTML += '<td>' + key + '</td>'; // Component
        tableHTML += '<td>' + components[key] + '</td>'; // Component Description
        tableHTML += '<td class="actions">';
        tableHTML += '<button class="edit-btn" onclick="editRow(this,event)">Edit</button>';
        tableHTML += '<button class="delete-btn" onclick="deleteRow(this,event)">Delete</button>';
        tableHTML += '</td>';
        tableHTML += '</tr>';
    }

    tableBody.html(tableHTML); // Inject the generated HTML into the table body
    $('#udresultTable').show(); // Show the table
    $('#udresultTable thead').show(); // Show the table header
}
$('#udresultBody').on('click', 'td', function (event) {
    event.stopPropagation();
});


function addComponent() {
    // Create a new row for adding a component
    var newRow = '<tr class="new-row">' +
        '<td><input type="text" class="editable" placeholder="New Component" maxlength="20"></td>' +
        '<td><input type="text" class="editable" placeholder="New Description" maxlength="20"></td>' +
        '<td class="actions">' +
        '<button class="save-btn" id="save-btn" onclick="saveNewRow(this,event)">Save</button>' +
        '<button class="cancel-btn" id="cancel-btn" onclick="cancelAddRow(this,event)">Cancel</button>' +
        '</td>' +
        '</tr>';

    // Append the new row at the end of the table
    $('#udresultBody').append(newRow);
}

function saveNewRow(button) {
    var newRow = $(button).closest('tr.new-row');
    var cells = newRow.find('td:not(.actions)');
    var newComponent = cells.eq(0).find('input').val();
    var newDescription = cells.eq(1).find('input').val();

    // Perform validation if needed

    if (newComponent && newDescription) {
        // Send the new data to the server
        $.ajax({
            type: "POST",
            url: "/add_new_component",
            data: { newComponent: newComponent, newDescription: newDescription },
            success: function (response) {
                console.log('New record added:', response);
                // Remove the new row upon successful addition
                newRow.remove();
                // Refresh the table with updated data
                fetchComponentData();
            },
            error: function (error) {
                console.error('Error adding new record:', error);
                // Handle error if needed
            }
        });
    } else {
        alert('Please provide both component and description values.');
        // Handle the case where either component or description is not provided
    }
}

function cancelAddRow(button) {
    // Remove the new row upon cancellation
    var newRow = $(button).closest('tr.new-row');
    newRow.remove();
}


var oldComponent, oldDescription;
function editRow(button, event) {
    console.log('Edit button clicked');

    var row = $(button).closest("tr");
    var cells = row.find("td:not(.actions)");
    event.stopPropagation();
    event.preventDefault();
    cells.each(function (index) {
        var cell = $(this);
        var cellText = cell.text();
        cell.attr('data-old-value', cellText);
        var maxLength = index === 0 ? 8 : 20; // 8 for the first cell, 20 for the second
        cell.html('<input type="text" class="editable" maxlength="' + maxLength + '" value="' + cellText + '">');
    });
    oldComponent = row.find('td:eq(0)').data('old-value');
    oldDescription = row.find('td:eq(1)').data('old-value');

    // Log values to console for debugging
    console.log('oldComponent:', oldComponent);
    console.log('oldDescription:', oldDescription);

    var actionsCell = row.find('.actions');
    actionsCell.html('<button class="save-btn" onclick="saveRow(this,event)">Save</button>' +
        '<button class="cancel-btn" onclick="cancelEditRow(this,event)">Cancel</button>');
    enableButtons(row);
}


// Function to cancel editing a row
function cancelEditRow(button) {
    var row = $(button).closest('tr');
    var cells = row.find('td:not(.actions)');

    cells.each(function () {
        var cell = $(this);
        var oldValue = cell.attr('data-old-value');
        cell.text(oldValue);
    });

    var actionsCell = row.find('.actions');
    actionsCell.html('<button class="edit-btn" onclick="editRow(this,event)">Edit</button>' +
        '<button class="delete-btn" onclick="deleteRow(this,event)">Delete</button>');
    enableButtons(row);

    // Preserve oldComponent and oldDescription
    oldComponent = cells.eq(0).text();
    oldDescription = cells.eq(1).text();
}


// Function to handle the save button click event
function saveRow(button) {
    var row = $(button).closest('tr');
    var cells = row.find('td:not(.actions)');
    var newData = []; // Array to hold modified data

    cells.each(function () {
        var cell = $(this);
        var input = cell.find('input');
        var newValue = input.val();
        cell.text(newValue); // Update cell with new value

        // Store new data in an array
        newData.push(newValue);
    });

    var payload = {
        oldComponent: oldComponent,
        oldDescription: oldDescription,
        newComponent: newData[0], // Updated component value after editing
        newDescription: newData[1]
    };

    var actionsCell = row.find('.actions');
    actionsCell.html('<button class="edit-btn">Edit</button>' +
        '<button class="delete-btn">Delete</button>');
    enableButtons(row);
    // Preserve oldComponent and oldDescription
    oldComponent = cells.eq(0).text();
    oldDescription = cells.eq(1).text();

    // Send the modified data to the server
    saveChangesToServer([payload]); // Wrap payload in an array

    // Reset oldComponent and oldDescription
    //oldComponent = null;
    //oldDescription = null;
}

function saveChangesToServer(payload) {
    console.log('Data sent to server:', payload);
    $.ajax({
        type: "POST",
        url: "/save_changes",
        contentType: "application/json",
        data: JSON.stringify({ components: payload }), // Wrap payload in an object
        success: function (response) {
            console.log('Response:', response);
            console.log(response.message);
            // Handle success
        },
        error: function (error) {
            console.error('Error:', error);
            // Handle error
        }
    })
        .always(function () {
            resetButtons();
        });
}

function deleteRow(button, event) {
    var row = $(button).closest("tr");
    var component = row.find('td:first').text(); // Assuming the Component column is the first one

    // Send a GET request to the server to get the count of associated masks
    $.ajax({
        type: "GET",
        url: "/get_mask_count",
        data: { component: component },
        success: function (response) {
            // Check if response has the 'result' property
            if ('result' in response && 'maskCount' in response.result) {
                var confirmationMessage = "Are you sure you want to delete this record?\n";
                confirmationMessage += "Number of Masks and Dictionaries effected: " + response.result.maskCount;

                // Use a JavaScript confirm dialog
                var confirmation = window.confirm(confirmationMessage);
                if (confirmation) {
                    // Send a POST request to the server for deletion
                    $.ajax({
                        type: "POST",
                        url: "/delete_record",
                        data: { component: component }, // Send the component to be deleted
                        success: function (response) {
                            console.log('Record deleted:', response);
                            row.remove(); // Remove the row from the table upon successful deletion
                        },
                        error: function (error) {
                            console.error('Error deleting record:', error);
                        }
                    });
                } else {
                    // Do nothing if the user selects "Cancel" in the confirmation dialog
                }
            } else {
                console.error('Invalid response format:', response);
            }
        },
        error: function (error) {
            console.error('Error getting mask count:', error);
        }
    });

    event.preventDefault(); // Prevent the default action of the button
    event.stopPropagation(); // Stop the event from propagating further
}



function resetButtons() {
    // Implement the logic to reset the buttons as needed
    // For example, enable the edit and delete buttons
    // Replace this with your actual logic
    $('.edit-btn').prop('disabled', false);
    $('.delete-btn').prop('disabled', false);
    // Reattach the click event for the edit button
    $('.edit-btn').off('click').on('click', function (event) {
        editRow(this, event);
    });
    $('.delete-btn').off('click').on('click', function (event) {
        deleteRow(this, event);
    });
}
function enableButtons(row) {
    row.find('.edit-btn').prop('disabled', false);
    row.find('.delete-btn').prop('disabled', false);
}

function disableButtons(row) {
    row.find('.edit-btn').prop('disabled', true);
    row.find('.delete-btn').prop('disabled', true);
}


$(document).on('click', '.edit-btn', function (event) {
    editRow(this, event);
});

$(document).on('click', '.save-btn', function (event) {
    saveRow(this, event);
});

$(document).on('click', '.cancel-btn', function (event) {
    cancelEditRow(this, event);
});