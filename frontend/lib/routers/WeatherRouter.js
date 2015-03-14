if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherRouter = (function(WeatherAppView) {
  var WeatherRouter = new (Backbone.Router.extend({
    routes: {
      'city/:id': 'city',
      '': 'index',
    },

    initialize: function(options) {
      this.weatherAppView = new WeatherAppView(/*{collection: this.travelList}*/)
    },

    start: function() {
      Backbone.history.start(/*{pushState: true}*/);
    },

    index: function() {
      this.weatherAppView.setElement($('#weather-app')).renderChooser();
    },

    city: function(id) {
      this.weatherAppView.setElement($('#weather-app')).render(id);
    },
  }));

  $(WeatherRouter.start);

  return WeatherRouter;
})(WeatherApp.WeatherAppView);