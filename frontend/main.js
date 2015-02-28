var WeatherPanel = Backbone.Model.extend({
  urlRoot: '/api/v0/weather',
  defaults: {
    id: 0,
    temperature: 0,
    windVelocity: 0,
    temperatureFeelsLike: 0,
    weatherInWords: 'Ясно понятно',
    image: '/PNG/simple_weather_icon_01.png',
    clothes: [{name: "Шуба", depth: 40, imgURL: "cosplay.png"}]
  }
});
var weatherPanel = new WeatherPanel({id: 55});
weatherPanel.fetch();


var WeatherPanelView = Backbone.View.extend({
  tagName: 'div',
  id: 'container',

  template: _.template([
    "<div id='humans'></div>",
    "<table id='panel'>",
    "<tr>",
    "<td class='weather-frame'>",
      "<div class='weather-tile'><img src=<%= image %>></div>",
      "<div class='weather-text'><span class='state'><%= weatherInWords %></span></div>",
    "</td>",
    "<td class='weather-frame'>",
      "<div class='weather-tile'><span class='kartinka' id='zaebalcya-pisat-po-english'><%= temperature %></span></div>",
      "<div class='weather-text'><span class='state'>Температура °С</span></div>",
    "</td>",
    "<td class='weather-frame'>",
      "<div class='weather-tile'><span class='kartinka' id='zaebalcya-pisat-po-english'><%= temperatureFeelsLike %></span></div>",
      "<div class='weather-text'><span class='state'>Ощущается °С</span></div>",
    "</td>",
    "</tr>",
    "</table>"
  ].join('')),

  initialize: function() {
    this.model.on('change', this.render, this);
    this.model.on('destroy', this.remove, this);
    this.model.on('hide', this.remove, this);
  },

  render: function(){
    this.$el.html(this.template(this.model.toJSON()));
    var backgroundImage = this.model.get('clothes')
      .sort(function(a, b) {
        return a.depth < b.depth;
      })
      .map(function(el) {
        return 'url(' + el.imgURL + ')'
      })
      .join(', ');
    $('#humans').css({backgroundImage:backgroundImage + ', url(background.png)'});
    return this;
  }
});

var view = new WeatherPanelView({model: weatherPanel});
view.render();
$('body').html(view.el);
