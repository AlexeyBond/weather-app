if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherPanelView = (function() {
  var WeatherPanelView = Backbone.View.extend({
    tagName: 'table',
    id: 'weather-panel',

    template: _.template([
      '<tr>',
        '<td class="weather-frame">',
          '<div class="weather-tile"><img src=<%= image %>></div>',
          '<div class="weather-text"><span class="state"><%= weatherInWords %></span></div>',
        '</td>',
        '<td class="weather-frame">',
          '<div class="weather-tile"><span class="kartinka" id="zaebalcya-pisat-po-english"><%= temperature %></span></div>',
          '<div class="weather-text"><span class="state">Температура °С</span></div>',
        '</td>',
        '<td class="weather-frame">',
          '<div class="weather-tile"><span class="kartinka" id="zaebalcya-pisat-po-english"><%= Math.round(temperatureFeelsLike) %></span></div>',
          '<div class="weather-text"><span class="state">Ощущается °С</span></div>',
        '</td>',
      '</tr>',
    ].join('\n')),

    initialize: function() {},

    render: function(){
      this.$el.html(this.template(this.model.toJSON()));
      return this;
    }
  });

  return WeatherPanelView;
})();