//import keys from "keys.js";
import { trashData } from './initFirestore.js'

console.log(trashData)
var script = document.createElement('script');
let map;


//let docRef = db.collection("trashlocation");
//let trashPoints = docRef.get();



script.src = 'https://maps.googleapis.com/maps/api/js?key=' + keys.googleMapsApiKey + '&libraries=visualization&callback=initMap';

script.async = false;
script.defer = false;
document.head.appendChild(script);
// Attach your callback function to the `window` object
let heatmapData = [];
let heatmapDataWeighted = [];
var querySnapshot;
window.addEventListener("DOMContentLoaded", async (e) => {
  querySnapshot = await trashData();
  console.log("query")
  visualize()
  
})
window.initMap = function(){
  console.log("initMap")
}

function visualize(){

  querySnapshot.forEach((doc) => {
    if(doc.get('lat')){
      var lat = doc.get('lat').toFixed(6)
      var lon = doc.get('lon').toFixed(6)
      //console.log(new google.maps.LatLng(37.774546, -122.433523))
      heatmapData.push(new google.maps.LatLng(lat, lon))
      heatmapDataWeighted.push({location: new google.maps.LatLng(lat, lon, doc.get('trash'))})
    }
  })

  var center = heatmapData[0];
  console.log("center")
  var maps = new google.maps.Map(document.getElementById('map'), {
    center: center,
    zoom: 7,
    mapTypeId: 'satellite'
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapDataWeighted
  });
  console.log("heatmap")
  heatmap.setMap(maps);

}


// Append the 'script' element to 'head'


/*
const loader = new Loader({
    apiKey: keys.googleMapsApiKey,
    version: "weekly",
    libraries: ["visualization"]
});*/
