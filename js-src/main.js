import $ from 'jquery'
import Bloodhound from 'bloodhound-js'

const SEARCH_URL = 'https://search.helpmanual.io/%QUERY'
// const SEARCH_URL = 'http://localhost:5000/%QUERY'

var search_source = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('name'),
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: SEARCH_URL
})

const EMPTY = '<div class="no-results">No results found</div>'
var $spinner = $('#spinner')
var $index = $('#index-content')

$('#search').typeahead({
  minLength: 2
}, {
  source: search_source,
  display: 'name',
  limit: 20,
  templates: {
    empty: EMPTY,
    suggestion: function(v) {
      return `<div>
  <div>
    <span class="tag tag-default">${v.src}</span>
    <b>${v.name}</b>
  </div>
  <div class="small">
    ${v.description}
  </div>
</div>`
    }
  }
}).on('typeahead:select', function(ev, suggestion) {
  window.location = suggestion.uri
}).on('typeahead:asyncrequest', function() {
  $spinner.show()
}).on('typeahead:asynccancel typeahead:asyncreceive', function() {
  $spinner.hide()
}).on('typeahead:active', function() {
  $index.fadeOut()
}).on('typeahead:idle', function() {
  $index.fadeIn()
})
