// Initialize map
function initMap() {
    const Dublin = { lat: 53.350140, lng: -6.266155 };
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 11,
      center: Dublin,
    });

    // Geographical Coordinates for each station

    const SmithfieldNorth = { lat: 53.349562, lng: -6.278198 };
    const ParnellSquareNorth = { lat: 53.3537415547453, lng: -6.26530144781526 };
    const ClonmelStreet = { lat: 53.336021, lng: -6.26298 };

  
    // Add markers for each Station
    const mk1 = new google.maps.Marker({
      position: SmithfieldNorth,
      title: "SmithField North",
      map: map,
    });

    const mk2 = new google.maps.Marker({
        position: ParnellSquareNorth,
        title: "Parnell Square North",
        map: map,
    });
    
      const mk3 = new google.maps.Marker({
        position: ClonmelStreet,
        title: "Clonmel Street",
        map: map,
    });
}
// Call initMap function when Google Maps API is loaded
google.maps.event.addDomListener(window, "load", initMap);