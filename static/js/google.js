function initMap() {

	var me = {
		info: '<strong>Sebastian Selin</strong><br>\
					Hällgumsgatan 25B<br> 87236 Kramfors<br>\
					<a href="http://jag2">www</a> <img src="http://i.imgur.com/xZDHKW9.jpg" alt="some_text" style="width:160px; height:160px;">',
					lat: 56.1864,
					long: 14.8498742
	};



	var locations = [
      [me.info, me.lat, me.long, 0],
      
        
    ];

	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 11,
		center: new google.maps.LatLng(56.164240, 14.866022),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	var infowindow = new google.maps.InfoWindow({});

	var marker, i;

	for (i = 0; i < locations.length; i++) {
		marker = new google.maps.Marker({
			position: new google.maps.LatLng(locations[i][1], locations[i][2]),
			map: map
		});

		google.maps.event.addListener(marker, 'click', (function (marker, i) {
			return function () {
				infowindow.setContent(locations[i][0]);
				infowindow.open(map, marker);
			}
		})(marker, i));
	}
}