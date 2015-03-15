if (window.WeatherApp === undefined) {
  WeatherApp = {};
}

WeatherApp.WeatherClothView = (function() {
  var WeatherClothView = Backbone.View.extend({
    tagName: 'img',
    class: 'weather-cloth',

    initialize: function() {
      this.attributes = {
        src: this.model.img
      };

      this.css = {
        position: 'relative',
        'z-index': this.model.zIndex
      };
    },

    render: function(){
      this.$el.css(this.css);
      return this;
    },
  });

  return WeatherClothView;
})();
