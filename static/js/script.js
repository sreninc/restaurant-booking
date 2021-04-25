document.addEventListener(
    'DOMContentLoaded', 
    function() {
        var elems = document.querySelectorAll('.sidenav');
        var instances = M.Sidenav.init(elems, {accordion: true, edge: 'right'});
        var textCounter = document.querySelectorAll('#message');
        M.CharacterCounter.init(textCounter);
    }
);

// Initiate modal functionality
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);
});

document.addEventListener('DOMContentLoaded', function() {
var elems = document.querySelectorAll('select');
var instances = M.FormSelect.init(elems, { dropdownOptions: {container: document.body, constrainWidth: true }} );
});

function editBooking(client_id, booking_id, booking_date, parent) {
    const row = document.getElementById("bookings-table").rows[parent].cells;

    document.getElementById("edit-booking-date").value = booking_date;
    document.getElementById("edit-booking-time").value = row[1].innerHTML;
    document.getElementById("edit-booking-people").value = row[3].innerHTML;
    document.getElementById("edit-booking-value").value = row[5].innerHTML.split("€")[1];

    var selectStatus = document.getElementById("edit-booking-status").options;
    for (i = 0; i < selectStatus.length; i++) {
        if (selectStatus[i].value == row[4].innerHTML.toLowerCase()) {
            selectStatus[i].selected = true;
        }
    }

    document.getElementById("edit-booking-id").value = booking_id;
    var select = document.getElementById("edit-booking-client-id").options;
    for (i = 0; i < select.length; i++) {
        if (select[i].value == client_id) {
            select[i].selected = true;
        }
    }
    var elem = document.querySelectorAll('.modal')[0];
    var instance = M.Modal.getInstance(elem);
    instance.open();

    var selectElems = document.querySelectorAll('select');
    selectElems[0].setAttribute("disabled", true);
    var selectInstances = M.FormSelect.init(selectElems, { dropdownOptions: {container: document.body, constrainWidth: true }} );
    
    M.updateTextFields();
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

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.fixed-action-btn');
    var instances = M.FloatingActionButton.init(elems);
});