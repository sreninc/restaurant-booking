function editBooking(booking_id, date) {
    var row = document.getElementById(booking_id).cells;
    document.getElementById("name").value = row[2].innerHTML.split(">")[1].split("<")[0];
    document.getElementById("date").value = date;
    document.getElementById("time").value = row[1].innerHTML;
    document.getElementById("people").value = row[3].innerHTML;

    const status = row[4].innerHTML;
    const statusSelect = document.getElementById("edit-booking-status").options;
    for (option in statusSelect) {
        if (statusSelect[option].innerHTML === status) {
            statusSelect[option].selected = true;
        }
    }
}

function editClient(clientId) {
    document.getElementById("editClient").value = clientId;
    var elem = document.querySelectorAll('.modal')[0];
    var instance = M.Modal.getInstance(elem);
    instance.open();

    const row = document.getElementById(clientId);
    var firstName = row.nextElementSibling;
    var lastName = firstName.nextElementSibling;
    var mobile = lastName.nextElementSibling;
    var email = mobile.nextElementSibling;
    
    firstName = firstName.innerHTML.trim();
    lastName = lastName.innerHTML.trim();
    email = email.innerHTML.trim();
    mobile = mobile.innerHTML.trim();

    document.getElementById("edit-client-firstname").value = firstName;
    document.getElementById("edit-client-lastname").value = lastName;
    document.getElementById("edit-client-email").value = email;
    document.getElementById("edit-client-mobile").value = mobile;

    M.updateTextFields();
}

function generateFlashMessage(message) {
    Swal.fire(message);
}
