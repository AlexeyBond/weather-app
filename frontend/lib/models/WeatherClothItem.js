if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherClothItem = (function() {
  var ClothItem = Backbone.Model.extend({
    urlRoot: '/api/v0/cloth/item',
    defaults: {
    },
  });

  return WeatherClothItem;
})();