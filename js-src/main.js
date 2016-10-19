import $ from 'jquery'
import Bloodhound from 'bloodhound-js'

const SEARCH_DOMAIN = 'https://search.helpmanual.io/'

var search_source = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: SEARCH_DOMAIN + '?query=%QUERY',
    wildcard: '%QUERY'
  }
})

const EMPTY = '<div>No results found</div>'

$('#search').typeahead({
  minLength: 2
}, {
  source: search_source,
  display: 'name',
  limit: 12,
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
})

$('#search').bind('typeahead:select', function(ev, suggestion) {
  window.location = suggestion.uri
})
