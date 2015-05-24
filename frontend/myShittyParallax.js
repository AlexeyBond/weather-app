function wind(obj, speed){
  var start = Date.now();
  var fps = 50;
  var timer = setInterval(function() {
    var timePassed = Date.now() - start;
    draw(obj,timePassed*speed);
  }, 20);
  obj.css({backgroundPosition: '200px 0px'});
}


function draw(obj,timePassed) {
  obj.css({backgroundPosition: timePassed+'px 0px'});
}