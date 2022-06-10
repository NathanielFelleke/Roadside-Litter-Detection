//import keys from "keys.js";
import { trashData } from './initFirestore.js'

console.log(trashData)
var script = document.createElement('script');
let map;

script.src = 'https://maps.googleapis.com/maps/api/js?key=' + keys.googleMapsApiKey + '&libraries=visualization&callback=initMap';

script.async = true;
document.head.appendChild(script);

let heatmapData = [];
let heatmapDataWeighted = [];
var querySnapshot;

window.addEventListener("DOMContentLoaded", async (e) => {
  querySnapshot = await trashData();
  console.log("query")
  visualize()
  
})



function visualize(){

  querySnapshot.forEach((doc) => {
    if(doc.get('lat')){
      var lat = doc.get('lat').toFixed(6)
      var lon = doc.get('lon').toFixed(6)
      heatmapData.push(new google.maps.LatLng(lat, lon))
      heatmapDataWeighted.push({location: new google.maps.LatLng(lat, lon, doc.get('trash'))})
    }
  })

  var center = heatmapData[0];

  var maps = new google.maps.Map(document.getElementById('map'), {
    center: center,
    zoom: 7,
    mapTypeId: 'satellite'
  });

  var heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData
  });

  heatmap.setMap(maps);
}

