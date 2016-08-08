// A lot of this could be done with jQuery but just practicing pure js.

function initialize() {
    var lat = document.getElementById('lat').innerHTML;
    var lon = document.getElementById('lon').innerHTML;
    var prop = {
    center:new google.maps.LatLng(lat,lon),
    zoom:15,
    mapTypeId:google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"),prop);
}

// Check to see if the map id exists and initialize if it does.

if (document.getElementById('map')){
    google.maps.event.addDomListener(window, 'load', initialize);
}

// Show or hide the time based on checkbox.
function showTime(){
    var checkbox = document.getElementById('showtime');
    if (checkbox.checked){
        time.style.display = 'block';
    }
    if (!checkbox.checked){
        time.style.display = 'none';
    }
}
