tilde.notices = {}

tilde.colors = ["#951F24","#C62026","#DD5524","#EF8F1E","#F2E74A","#A0F582"] //["#951F24","#F2E3E4"]
tilde.risks = [1,.89,.75,.45,.2,0] //[1,0]

tilde.needleScale = d3.scale.linear().domain([0.502,0.731438356]).range([0,1])

tilde.updateNeedle = function() {
	d3.selectAll('.needle, .needle-center').style('opacity',0)
	var data = tilde.current_selection;
	d3.select("#needle")
		.transition()
		.duration(500)
		.style('opacity',1)
	needle.moveTo(tilde.needleScale(data.ai))
	d3.select(".chart-filled")
		.style('fill',tilde.colorScale(data.ai))

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
			.text("Predicted impact of automation")
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
			.text("(gauge is relative to all cities studied)")
			.attr('text-anchor','middle')
			.style('font-style','italic')
			
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
			.text(round(data.ai*100,1)+'%')
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
			.text(round(data.ai*100,1)+'%')
			.style('opacity',0)
			.transition()
			.duration(800)
			.style('opacity',1)	
	}
}