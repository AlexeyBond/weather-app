if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherClothesCollection = (function(WeatherClothItem) {
  var WeatherClothesCollection = Backbone.Collection.extend({
    url: '/api/v0/cloth/choose',
    model: WeatherClothItem,
  });

  return WeatherClothesCollection;
})(WeatherApp.WeatherClothItem);