function viewDiv(){
    var hidden = document.getElementsByClassName('extra_bouquets');
    var i;
    for (i = 0; i < hidden.length; i++) {
        hidden[i].style.display = "block";
    }
    document.getElementById('more_bouquets').style.display = 'None';
};