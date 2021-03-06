function editBooking(booking_id, date, guestId) {
    var row = document.getElementById(booking_id).cells;
    document.getElementById("name").value = row[2].innerHTML.split(">")[1].split("<")[0];
    document.getElementById("guestId").value = guestId;
    document.getElementById("bookingId").value = booking_id;
    document.getElementById("date").value = date;
    document.getElementById("time").value = row[1].innerHTML;
    document.getElementById("people").value = row[3].innerHTML;
    document.getElementById("value").value = row[6].innerHTML;

    const status = row[4].innerHTML;
    const statusSelect = document.getElementById("edit-booking-status").options;
    for (option in statusSelect) {
        if (statusSelect[option].innerHTML === status) {
            statusSelect[option].selected = true;
        }
    }
}

function addBooking(guestFirst, guestLast, guestId) {
    guest = guestFirst + " " + guestLast;
    document.getElementById("add-name").value = guest;
    document.getElementById("add-guestId").value = guestId;
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

function editUser(userId, access, email, name) {
    document.getElementById("access").value = access;
    document.getElementById("userId").value = userId;
    document.getElementById("email").value = email;
    document.getElementById("name").value = name;

    const accessSelect = document.getElementById("access").options;
    for (option in accessSelect) {
        if (accessSelect[option].value === access) {
            accessSelect[option].selected = true;
        }
    }
}

function generateFlashMessage(message) {
    Swal.fire(message);
}

function confirmDeleteBooking(bookingId, clientId, value, status) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href="/delete_booking/" + bookingId + "/" + clientId + "/" + value + "/" + status;
        }
    })
}

function confirmDeleteGuest(clientId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href="/delete_client/" + clientId;
        }
    })
}

function confirmDeleteUser(userId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href="/delete_user/" + userId;
        }
    })
}