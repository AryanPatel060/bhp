function onClickedEstimatePrice() {
      console.log("Estimate price button clicked");
      var sqft = document.getElementById("uiSqft");
      var bhk = document.getElementById("uiBHK");
      var bathrooms = document.getElementById("uiBathrooms");
      var location = document.getElementById("uiLocations");
      
      
      var url = "http://127.0.0.1:5000/predict_home_price";
      data={
        total_sqft: parseFloat(sqft.value),
        bhk: bhk.value,
        bath: bathrooms.value,
        location: location.value
    }
    sendDataToServer(data)
    //   $.post(url, {
    //       total_sqft: parseFloat(sqft.value),
    //       bhk: bhk,
    //       bath: bathrooms,
    //       location: location.value
    //   },function(data, status) {
    //       console.log(data.estimated_price);
    //       estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
    //       console.log(status);
    //   });
      }

function onPageLoad(){
      var counter = 0;
        var jsonObj;
        var stringify, obj;
        console.log( "document loaded" );
        var url = "http://127.0.0.1:5000/get_location_name"; 
        var xmlhttp = new XMLHttpRequest();

        xmlhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var data = JSON.parse(this.responseText);
                if(data){
                var locations = data.locations;
                var uiLocations = document.getElementById("uiLocations");
                $('#uiLocations').empty();
                for(var i in locations) {
                    var opt = new Option(locations[i]);
                    $('#uiLocations').append(opt);
                }
            }
            }
        };
        xmlhttp.open("GET", url, true);
        xmlhttp.send();
        }

        window.onload = onPageLoad;

        function sendDataToServer(data) {
        var xhr = new XMLHttpRequest();
        var estPrice = document.getElementById("uiEstimatedPrice");
        var url = "http://127.0.0.1:5000/predict_home_price"; // Replace with your server URL and endpoint
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
        xhr.send(JSON.stringify(data));

        xhr.onload = function () {
            if (xhr.status === 200) {
            // Handle a successful response from the server
            var response = JSON.parse(xhr.responseText);
            console.log('Response from server:', response);
            estPrice.innerHTML = "<h4>" + response.price.toString() + " Lakh</h4>";
            } else {
            // Handle errors here
            console.error('Error sending data to server:', xhr.statusText);
            }
        };

}