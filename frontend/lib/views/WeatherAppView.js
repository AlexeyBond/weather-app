if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherAppView = (function(
  WeatherCondition,
  WeatherClothesCollection,
  WeatherPanelView,
  WeatherClothesView
) {
  var WeatherAppView = Backbone.View.extend({
    tagName: 'div',
    id: 'weather-app',

    templateChooser: _.template('<a href="#/city/28698">Omsk</a>'),

    template: _.template([
      '<div id="weather-clothes"></div>',
      '<table id="weather-panel"></table>'
    ].join('\n')),

    initialize: function() {},

    renderChooser: function() {
      this.$el.html(this.templateChooser());
      return this;
    },

    render: function(id) {
      this.weatherCondition = new WeatherCondition({id: id});
      this.weatherClothesCollection = new WeatherClothesCollection({
        temperature: this.weatherCondition.get('temperature'),
        windVelocity: this.weatherCondition.get('windVelocity'),
        temperature: this.weatherCondition.get('season'),
      });

      this.weatherPanelView = new WeatherPanelView({model: this.weatherCondition});
      this.weatherClothesView = new WeatherClothesView({collection: this.weatherClothesCollection});

      this.$el.html(this.template());
      this.weatherPanelView.setElement(this.$('#weather-panel')).render();
      this.weatherClothesView.setElement(this.$('#weather-clothes')).render();

      return this;
    },
  });

  return WeatherAppView;
})(
  WeatherApp.WeatherCondition,
  WeatherApp.WeatherClothesCollection,
  WeatherApp.WeatherPanelView,
  WeatherApp.WeatherClothesView
);