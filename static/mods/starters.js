// < or > 0 randomizer
function rnd2() {
	return ((Math.random() + Math.random() + Math.random() + Math.random() + Math.random() + Math.random()) - 3) / 3;
}

/* changing the layout order is called like this:
	circles.on("mouseover",function(){
		var sel = d3.select(this);
		sel.moveToFront();
	});
*/
d3.selection.prototype.moveToFront = function() {
	this.each(function(){ this.parentNode.appendChild(this); });
};

//helpful rounding function
function round(value, decimals) {
  return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
}

//Transition callback runs when ALL elements have finished
function endall(transition, callback) { 
	var n = 0; 
	transition 
		.each(function() { ++n; }) 
		.each("end", function() { if (!--n) callback.apply(this, arguments); }); 
}


// Fisher-Yates Shuffle
function shuffle(array) {
	var m = array.length, t, i;
	while (m) {
		i = Math.floor(Math.random() * m--);
		t = array[m];
		array[m] = array[i];
		array[i] = t;
	}
	return array;
}