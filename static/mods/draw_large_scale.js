tilde.notices = {}

//tilde.colors = ["#951F24","#C62026","#DD5524","#EF8F1E","#F2E74A","#A0F582"] //["#951F24","#F2E3E4"]
//tilde.risks = [1,.89,.75,.45,.2,0] //[1,0]

tilde.ai_rank_domain = [1,0.8,0.6,0.4,0.2,0]
tilde.rank_color_range = ["#951F24","#C62026","#DD5524","#EF8F1E","#F2E74A","#A0F582"]
tilde.rank_color_scale = d3.scale.linear().domain(tilde.ai_rank_domain).range(tilde.rank_color_range)

//tilde.colors = ["#951F24","#C62026","#DD5524","#EF8F1E","#F2E74A","#A0F582"] //["#951F24","#F2E3E4"]
//tilde.risks = [1,.8,.6,.4,.2,0] //[1,0]

//tilde.needleScale = d3.scale.linear().domain([0.502,0.731438356]).range([0,1])
tilde.needleScale = d3.scale.linear().domain([0,100]).range([0,1])

function get_ai_task_rank_percent(data){
	var num_city = 0;
	num_city = tilde.cities.length;

	var ai_task_rank = 1
  
	for (var num = 0; num < tilde.cities.length; num++) {
	  var d = tilde.cities[num];
	
		if (data.ai_task_type < d.ai_task_type) {
		  ai_task_rank = ai_task_rank + 1;
		}
	}
	return Math.round(ai_task_rank/num_city*100);
  }  

tilde.updateNeedle = function() {
	d3.selectAll('.needle, .needle-center').style('opacity',0)
	var data = tilde.current_selection;

	var ai_task_rank_pct = get_ai_task_rank_percent(data);

	d3.select("#needle")
		.transition()
		.duration(500)
		.style('opacity',1)
	needle.moveTo(tilde.needleScale(ai_task_rank_pct))

	console.log(ai_task_rank_pct/100);
	console.log(tilde.rank_color_scale(ai_task_rank_pct/100));

	d3.select(".chart-filled")
		.style('fill',tilde.rank_color_scale(ai_task_rank_pct/100))

	if (!d3.select("#needle_annotation").node()) {
		tilde.annotation = d3.select("#sub_wrapper")
			.append('div')
			.attr("id","needle_annotation")

		var svg = tilde.annotation	
			.append('svg')
			.attr('width',function(d,i){
				var x = +d3.select("#needle_annotation")[0][0].offsetWidth
					return x
			})
			.attr('height',function(d,i){
				var x = +d3.select("#needle_annotation")[0][0].offsetWidth/4 + tilde.dropheight
					return x
			})
			
		//var translate = d3.select('#needle g').attr('transform')
		var g = svg	
			.append('g')
			.attr('transform',"translate(0, " + tilde.dropheight + ")")
			
		var first = g
			.append("text")
			.text("Predicted")
			.attr('text-anchor','middle')
			.style('font-weight','bold')
			
		first.attr('y',function(d,i){
				var y = +d3.select(this).node().getBBox().height*1.1
				return y
			})
			.attr('x',function(d,i){
				var x = +d3.select("#needle_annotation")[0][0].offsetWidth/2
				return x
			})
			.style('font-size',function(d,i){
				return d3.select(this).style('font-size')
			})
			.style('opacity',0)
			.transition()
			.duration(1200)
			.style('opacity',1)
		
		
		var second = g
			.append("text")
			.text(data['task_type'])
			.attr('text-anchor','middle')
			.style('font-weight','bold')
			
		second.attr('y',function(d,i){
				var y = (+d3.select(this).node().getBBox().height)*2.2
				return y
			})
			.attr('x',function(d,i){
				var x = +d3.select("#needle_annotation")[0][0].offsetWidth/2
				return x
			})
			.style('font-size',function(d,i){
				return d3.select(this).style('font-size')
			})
			.style('opacity',0)
			.transition()
			.duration(1200)
			.style('opacity',1)
		

		var g = svg	
			.append('g')
			.attr('transform',"translate(0, " + tilde.dropheight/1.3 + ")")
			.style('z-index','500')

		tilde.target = g
			.append("text")
			.text('Top '.concat(String(round(ai_task_rank_pct,2)),'%'))
			.attr('text-anchor','middle')
			.style('font-weight','bold')

		tilde.target.attr('y',function(d,i){
				var y = (+d3.select(this).node().getBBox().height)
				return y
			})
			.attr('x',function(d,i){
				var x = +d3.select("#needle_annotation")[0][0].offsetWidth/2.1
				return x
			})
			.style('font-size',function(d,i){
				var newsize = d3.select(this).style('font-size')
				newsize = (+newsize.substring(0,newsize.length-2))*2.5
				return newsize+'px'
			})
			.style('opacity',0)
			.transition()
			.duration(1200)
			.style('opacity',1)	
	} else {
		tilde.target
			.text('Top '.concat(String(round(ai_task_rank_pct,2)),'%'))
			.style('opacity',0)
			.transition()
			.duration(800)
			.style('opacity',1)	
	}
}