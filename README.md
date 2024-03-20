# Onkabetse

{% extends 'project_content/base.html' %}
{% block content %}
<div class="pageholder">
    <div class="titleholder"> 
        <div class="title"> Google Maps to track your order </div> 
    </div>

    <div id="map" style="height: 400px; width: 100%;"></div>

    <form id="locationForm">
        <label for="origin">Enter Your Location:</label>
        <input type="text" id="origin" name="origin"><br><br>
        
        <input type="submit" value="Submit">
    </form>

    <div id="etaDisplay">
        <p>Estimated Time of Arrival: <span id="eta"></span></p>
    </div>
</div>


<script>
    const updateFrequency = 1000; // milliseconds (1 second)

    async function trackDelivery() {
        try {
            const response = await fetch('/api/delivery-route');
            const data = await response.json();

            if (!data.routeCoordinates || !Array.isArray(data.routeCoordinates)) {
                throw new Error('Invalid route data');
            }

            const routeCoordinates = data.routeCoordinates;

            for (let index = 0; index < routeCoordinates.length; index++) {
                const coordinate = routeCoordinates[index];
                await new Promise(resolve => setTimeout(resolve, index * updateFrequency));
                updateDeliveryMarker(coordinate);
            }
        } catch (error) {
            console.error('Error fetching or tracking delivery:', error);
        }
    }

    window.initMap = initMap;

    document.getElementById('locationForm').addEventListener('submit', handleSubmit);
    trackDelivery(); // Start tracking delivery when the page loads

    var map;
    var directionsService;
    var directionsRenderer;
    var deliveryMarker;
    var etaDisplay = document.getElementById('eta'); 

    function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 12,
            center: { lat: -25.4808, lng: 28.1036 } 
        });
        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);
        
        // Icon B: New deliveryMarker configuration
  // Icon B: New deliveryMarker configuration
  deliveryMarker = new google.maps.Marker({
    map: map,
    icon: {
        path: deliveryMarker = new google.maps.Marker({
    map: map,
    icon: {
        path: '<a href="https://iconscout.com/icons/car" class="text-underline font-size-sm" target="_blank">Car</a> by <a href="https://iconscout.com/contributors/icograms" class="text-underline font-size-sm">Icograms</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>',
        fillColor: '#000000',
        fillOpacity: 1,
        strokeWeight: 0,
        scale: 1.5,
        rotation: 90,
        anchor: new google.maps.Point(8, 8)
    },
    title: 'Delivery Vehicle'
}),

        fillColor: '#000000',
        fillOpacity: 1,
        strokeWeight: 0,
        scale: 1.5,
        rotation: 90,
        anchor: new google.maps.Point(8, 8)
    },
    title: 'Delivery Vehicle'
});


    }
    
    function calculateRoute(destination) {
        var origin = { lat: -25.5502, lng: 28.0897 }; // Set the vehicle's origin to the specified coordinates
        var request = {
            origin: origin,
            destination: destination,
            travelMode: 'DRIVING'
        };
        directionsService.route(request, function(result, status) {
            if (status == 'OK') {
                directionsRenderer.setDirections(result);
                animateDeliveryMarker(result, destination); // Start animation from the destination entered by the user

                var route = result.routes[0];
                var legs = route.legs;
                var duration = 0;
                for (var i = 0; i < legs.length; i++) {
                    duration += legs[i].duration.value;
                }
                var minutes = Math.round(duration / 60);
                document.getElementById('eta').innerText = minutes + ' minutes';
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
    }

    function animateDeliveryMarker(route, startLocation, estimatedTime) {
        var path = route.routes[0].overview_path;
        var numSteps = path.length;
        var totalDistance = 0;

        // Calculate total distance of the path
        for (var i = 1; i < numSteps; i++) {
            totalDistance += google.maps.geometry.spherical.computeDistanceBetween(path[i - 1], path[i]);
        }

        // Calculate speed dynamically based on the total distance and estimated time
        var speed = totalDistance / (estimatedTime * 60); // in meters per second

        // Function to update the marker's position
        function updateDeliveryMarker(position) {
            deliveryMarker.setPosition(position);
        }

        // Function to move the marker along the path

        function moveMarker() {
        var index = 0;
        var interval = setInterval(function() {
        if (index < numSteps) {
            var newPosition = path[index];
            updateDeliveryMarker(newPosition); // Update delivery marker position
            index++;
        } else {
            clearInterval(interval); // Stop the animation when all steps are covered
        }
    }, 2000); // Set a longer interval (in milliseconds) to slow down the movement, e.g., 2000 milliseconds (2 seconds)
}


        // Start the animation from the specified startLocation
        moveMarker();
    }

    function handleSubmit(event) {
        event.preventDefault();
        var origin = document.getElementById('origin').value;
        calculateRoute(origin);
    }
</script>

<script async src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCZJCJVzkTMgNFmi6SXU3IVcRiUt6luZIk&callback=initMap"></script>
{% endblock %}
