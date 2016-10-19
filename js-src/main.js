import $ from 'jquery'
import Bloodhound from 'bloodhound-js'

const SEARCH_DOMAIN = 'https://search.helpmanual.io/'
// const SEARCH_DOMAIN = 'http://localhost:5000/'

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
  hint: true,
  highlight: true,
  minLength: 2
}, {
  source: search_source,
  display: 'name',
  limit: 12,
  templates: {
    empty: EMPTY,
    suggestion: function(v) {
      return `<div><b>${v.name}</b> – <span>${v.descr}</span></div>`
    }
  }
})

$('#search').bind('typeahead:select', function(ev, suggestion) {
  console.log('Selection: ', suggestion)
  window.location = suggestion.uri
})
