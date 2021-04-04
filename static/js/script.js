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