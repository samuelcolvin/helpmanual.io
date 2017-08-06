import $ from 'jquery'
import Bloodhound from 'bloodhound-js'

window.ga('create', 'UA-62733018-3', 'auto')
window.ga('send', 'pageview')

const SEARCH_URL = 'https://search.helpmanual.io/q/{query}'
// const SEARCH_URL = 'http://localhost:5000/q/{query}'

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
let $search = $('#search')

$search.typeahead({
  minLength: 2
}, {
  source: search_source,
  display: 'name',
  limit: 20,
  templates: {
    empty: EMPTY,
    suggestion: (v) => `<div>
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
).on('typeahead:select', (ev, suggestion) => {
  window.ga('send', 'event', {
    eventCategory: 'Search',
    eventAction: 'select',
    eventLabel: suggestion.uri
  })
  go_to(suggestion.uri, true)
}
).on('typeahead:asyncrequest', () => $spinner.show()
).on('typeahead:asynccancel typeahead:asyncreceive', () => $spinner.hide()
)

// very useful during development:
// $(document).on('typeahead:beforeclose', (event) => event.preventDefault())

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

window.onscroll = () => {
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

  $dynamic.load(uri + ' #dynamic', (response, status, xhr) => {
    if (status === 'error') {
      console.error('Error getting uri', uri, xhr)
      window.location = uri
      return
    }
    $dynamic.stop(true, false)
    push && history.pushState(null, '', uri)

    window.ga('set', 'page', uri)
    window.ga('send', 'pageview')

    $dynamic.fadeIn(200)
    // reset stuff after "going to" the new page
    page_change()
    prepare_scroll()
    $search.typeahead('val', '')
    document.title = $dynamic.find('h1').first().text()
  })
  return false
}

function google_ads () {
  if (!window.adsbygoogle) {
    // adsbygoogle js isn't loaded yet
    window.adsbygoogle = [{}]
  } else if ($('.adsbygoogle').not('[data-adsbygoogle-status]').length) {
    // adsbygoogle is loaded and there are elements which haven't been initialised
    window.adsbygoogle.push({})
  }
}

function page_change() {
  setTimeout(() => $('#search').focus(), 50)
  google_ads()
  let $a = $('a')
  $a.unbind('click')
  $a.click(function () {
    let $this = $(this)
    if ($this.hasClass('no-page')) {
      return false
    } else {
      return go_to($this.attr('href'), true)
    }
  })
}

$(window).on('popstate', () => go_to(window.location.pathname, false))

function draw () {
  let c = $('canvas')[0].getContext('2d')
  let s = 25
  let w = window.innerWidth
  if (w < 1000) {
    // don't render on mobile
    return
  }
  c.canvas.width  = w
  let h = 370
  c.canvas.height = h
  let light_random = 3

  function hex (x_, y_) {
    // 42587f == hsl(218, 32%, 38%)
    let light = 38 + Math.random() * light_random - light_random / 2
    c.fillStyle = 'hsl(218, 32%, ' + light + '%)'
    c.beginPath()
    c.moveTo(y_, x_)
    c.lineTo(y_ + s, x_ + s * 0.5)
    c.lineTo(y_ + s, x_ + s * 1.5)
    c.lineTo(y_, x_ + s * 2)
    c.lineTo(y_ - s, x_ + s * 1.5)
    c.lineTo(y_ - s, x_ + s * 0.5)
    c.fill()
    c.closePath()
  }

  let x_step = s * 1.5
  for (let i = 0; i < h / x_step; i++) {
    let x = i * x_step
    let y_start = i % 2 === 0 ? 0 : s
    for (let y = y_start; y < w + s; y += s * 2) {
      hex(x, y)
    }
  }
}

$(document).ready(() => {
  page_change()
  draw()
})

$(window).resize(draw)
