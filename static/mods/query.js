tilde.query = {}
tilde.unlocked = true

tilde.query.select = function(source,input) {
	tilde[source][input].c = input
	return tilde[source][input]
}
tilde.query.selectAll = function(source,input_array) {
	if (input_array.constructor === Array) {
		var output = [],
			j = input_array.length,
			i;
		for (i = 0; i < j; i++) {
			tilde[source][input_array[i]].c = input_array[i]
			output.push(tilde[source][input_array[i]])
		}
		return output
	} else {
		tilde[source][input].c = input
		return tilde[source][input]
	}
}
tilde.query.prepareData = function() {
	var data = tilde.current_selection;
	tilde.map.move()
	tilde.map.mark()
	tilde.updateNeedle()
}