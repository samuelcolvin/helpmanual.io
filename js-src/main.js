import $ from 'jquery'
import Bloodhound from 'bloodhound-js'

const SEARCH_URL = 'https://search.helpmanual.io/{query}'
// const SEARCH_URL = 'http://localhost:5000/{query}'

let search_source = new Bloodhound({
  datumTokenizer: Bloodhound.tokenizers.whitespace,
  queryTokenizer: Bloodhound.tokenizers.whitespace,
  remote: {
    url: SEARCH_URL,
    wildcard: '{query}'
  }
})

const EMPTY = '<div class="no-results">No results found</div>'
let $spinner = $('#spinner')
let $index = $('#index-content')
let $search = $('#search')

$search.typeahead({
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
    <span class="tag">${v.src}</span>
    <b>${v.name}</b>
  </div>
  <small>
    ${v.description}
  </small>
</div>`
    }
  }
}).on('typeahead:select', function(ev, suggestion) {
  go_to(suggestion.uri, true)
}).on('typeahead:asyncrequest', function() {
  $spinner.show()
}).on('typeahead:asynccancel typeahead:asyncreceive', function() {
  $spinner.hide()
}).on('typeahead:active', function() {
  $index.fadeOut()
}).on('typeahead:idle', function() {
  $index.fadeIn()
})

$('.navbar .container').show()

// affix extra header
let $alt_head
let head_limit = 70
let alt_head_shown = false
function prepare_scroll() {
  $alt_head = $('#alt-head')
  if (window.pageYOffset > head_limit) {
    $alt_head.show()
    alt_head_shown = true
  }
}
prepare_scroll()

window.onscroll = function() {
  if(window.pageYOffset > head_limit){
    if (!alt_head_shown) {
      $alt_head.fadeIn(200)
      alt_head_shown = true
    }
  } else {
    if (alt_head_shown) {
      $alt_head.fadeOut(200)
      alt_head_shown = false
    }
  }
}

let $dynamic = $('#dynamic')

function go_to(uri, push){
  if (!uri.startsWith('/')) {
    return true
  }
  $dynamic.fadeOut(2000)

  $dynamic.load(uri + ' #dynamic', function( response, status, xhr ) {
    if (status == 'error') {
      console.error('Error getting uri', uri, xhr)
      window.location = uri
      return
    }
    $dynamic.stop(true, false)
    if (push === true){
      history.pushState(uri, '', uri)
    }
    $dynamic.fadeIn(200)
    // reset stuff after "going to" the new page
    a_click()
    prepare_scroll()
    $search.typeahead('val', '')
    document.title = $dynamic.find('h1').first().text()
  })
  return false
}

function a_click() {
  let $a = $('a')
  $a.unbind('click')
  $a.click(function () {
    return go_to($(this).attr('href'), true)
  })
}

$(document).ready(a_click)

$(window).on('popstate', function() {
  go_to(window.location.pathname, false)
})
