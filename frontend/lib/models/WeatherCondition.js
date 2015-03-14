if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherCondition = (function() {
  var WeatherCondition = Backbone.Model.extend({
    urlRoot: '/api/v0/weather',
    defaults: {
      id: '',
      temperature: '',
      windVelocity: '',
      temperatureFeelsLike: '',
      weatherInWords: '',
      image: '/PNG/simple_weather_icon_00.png',
      clothes: []
    }
  });

  return WeatherCondition;
})();