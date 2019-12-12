tilde.cities.forEach(function(d){
    //console.log(d)
    var newLocation = '',
        j = d.Location.length,
        i;
    for (i = 0; i < j; i++) {
        var str = d.Location.substring(i,i+1)
        if (str === ',') {
            str = d.Location.substring(i,j)
            newLocation += str
            break
        }
        if (str === '-') {
            str = ' - '
        }
        newLocation += str
    }
    d.Location = newLocation
})

// Constructing the suggestion engine
tilde.bloodhound = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace('Location'),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    identify: function(obj){ return obj.Location; },
    local: tilde.cities
});

tilde.bloodhound.initialize()

// Initializing the typeahead
$('#job_dropdown .typeahead').typeahead({
    hint: true,
    highlight: true, /* Enable substring highlighting */
    minLength: 1 /* Specify minimum characters required for showing suggestions */
},
{
    name: 'cities',
    displayKey: 'Location',
    source: tilde.bloodhound,
    templates: {
        empty: [
          '<div class="empty-message">',
            "No results, try something else...",
          '</div>'
        ].join('\n')
      }
});

$('#job_dropdown .typeahead').bind('typeahead:selected', function(obj, datum, name) {  
    tilde.current_selection = datum
    tilde.query.prepareData()
    $('input').blur()
});