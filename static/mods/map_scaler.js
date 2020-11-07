tilde.map = L.map('map');
tilde.map.scrollWheelZoom.disable()

var ai_risk_min = 100
var ai_risk_max = -100

var employment_min = 1000000
var employment_max = 0

function get_ai_rank(data){
  var ai_rank = 1

  for (var num = 0; num < tilde.cities.length; num++) {
    var d = tilde.cities[num];
  
    if (data.ai < d.ai) {
      ai_rank = ai_rank + 1;
    }
  }
  return ai_rank;
}

function get_ai_task_rank(data){
  var ai_task_rank = 1

  for (var num = 0; num < tilde.cities.length; num++) {
    var d = tilde.cities[num];
  
      if (data.ai_task_type < d.ai_task_type) {
        ai_task_rank = ai_task_rank + 1;
      }
  }
  return ai_task_rank;  
}  

for (var num = 0; num < tilde.cities.length; num++) {
  var d = tilde.cities[num];
  if (d.ai < ai_risk_min){
    ai_risk_min = d.ai_task_type;
  }
  if (d.ai > ai_risk_max){
    ai_risk_max = d.ai_task_type;
  }
  if (d.employment < employment_min){
    employment_min = d.employment;
  }
  if (d.employment > employment_max){
    employment_max = d.employment;
  }  
}

var num_city = 0
num_city = tilde.cities.length;

tilde.employmentDomain = [employment_min-10000,employment_max+10000]
tilde.ai_riskDomain = [ai_risk_min-0.01,(ai_risk_min+ai_risk_max)/2,ai_risk_max+0.01]

tilde.colorRange = ["#FAE1E1","#EB97A8","#DC143C"]
tilde.radiusScale = d3.scale.linear().domain(tilde.employmentDomain).range([1500,54000])
tilde.colorScale = d3.scale.linear().domain(tilde.ai_riskDomain).range(tilde.colorRange)
tilde.token = 'pk.eyJ1Ijoiam9uZ2hvIiwiYSI6ImNqNXVwNDVxMzBvYW8yeWtmeWlpb3pmb28ifQ.Eei6uDn--hcmZ6M3ZNXjGg'

tilde.map.circleGroup = L.featureGroup().addTo(tilde.map);
tilde.map.markerGroup = L.layerGroup().addTo(tilde.map);
if ($(window).width() < 750) {
  tilde.map.setView([39.8283, -98.5795], 3);
}
else {
  tilde.map.setView([39.8283, -98.5795], 4);
}

tilde.gl = L.mapboxGL({
    style: 'mapbox://styles/jongho/ck454q6nm009i1cpdjnbwj591',
    accessToken: tilde.token,
    attribution: 'Style: <a href="https://twitter.com/rasagy">@rasagy</a> | &copy; <a href="https://www.mapbox.com/about/maps/">Mapbox</a> | &copy; <a href="http://osm.org/copyright">OpenStreetMap</a> | <a href="https://www.mapbox.com/map-feedback/"><b>Improve this map</b></a>'
}).addTo(tilde.map);

for (var num = 0; num < tilde.cities.length; num++) {
  var d = tilde.cities[num];
  var place_lat = d["Lat"];
  var place_long = d["Lng"];

  var circle = L.circle([place_lat, place_long], {
      color: tilde.colorScale(d.ai_task_type),
      stroke: false,
      fillOpacity:.95,
      data: d,
      radius: 314*Math.sqrt(tilde.radiusScale(d.e))
  }).addTo(tilde.map.circleGroup)
}
tilde.circles = d3.selectAll('.leaflet-interactive').style('mix-blend-mode','screen')

tilde.map.on('zoomend', function() {
  if (tilde.map.getZoom() > 11) {
    tilde.circles
      .transition()
      .duration(900)
      .style('opacity','0')
  } else if (tilde.map.getZoom() > 8) {
    tilde.circles
      .transition()
      .duration(900)
      .style('opacity','0.3')
  } else {
    tilde.circles
      .style('opacity','0.95')
  }
})

tilde.map.circleGroup.on('click',function(e){
  tilde.map.circleClick(e)
});

tilde.map.move = function() {
  var data = tilde.current_selection;
  tilde.map.flyTo([data.Lat, data.Lng],8);
}

tilde.map.mark = function() {
  var data = tilde.current_selection;
  tilde.map.markerGroup.clearLayers()
  tilde.marker = L.marker([data.Lat, data.Lng]).addTo(tilde.map.markerGroup)
  var popup_html = '<h3><b>' + data['Location'] + '</b></h3><p><b>Year</b>: '+data.year+   '<br><b>Employment</b>: ' +data.employment+  '<br><b>Automation Index</b>: ' +round(data.ai*100,2)+'% (' +get_ai_rank(data)+ '/'+num_city+')<br><b>'+  data['task_type']+'</b>: '+ +round(data.ai_task_type*100,2) +'% ('+ get_ai_task_rank(data) +'/'+ num_city + ')</p>';  
  tilde.marker.bindPopup(popup_html);
  tilde.marker.openPopup()
}

tilde.map.circleClick = function(e) {
  tilde.current_selection = e.layer.options.data
  tilde.query.prepareData()
}