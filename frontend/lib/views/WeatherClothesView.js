if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherClothesView = (function() {
  var WeatherClothesView = Backbone.View.extend({
    tagName: 'div',
    id: 'weather-clothes',

    initialize: function() {
      this.listenTo(this.collection, 'add', this.addOne);
    },

    render: function(){
      this.$el.empty();
      this.addAll();
      return this;
    },

    addAll: function() {
      this.collection.forEach(this.addOne, this);
    },

    addOne: function(clothItem) {
      var weatherClothView = new WeatherApp.WeatherClothView({model: clothItem});
      this.$el.append(weatherClothView.render().el);
    },
  });

  return WeatherClothesView;
})();
