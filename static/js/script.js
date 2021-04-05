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

function addBooking(clientId) {
    document.getElementById("clientId").value = clientId;
    var elem = document.querySelectorAll('.modal')[1];
    var instance = M.Modal.getInstance(elem);
    instance.open();
}