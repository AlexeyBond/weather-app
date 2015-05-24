function wind(obj, speed){
  var start = Date.now();
  var timer = setInterval(function() {
    var timePassed = Date.now() - start;
    draw(obj,timePassed*speed);
  }, 50);
  obj.css({backgroundPosition: '200px 0px'});
}


function draw(obj,timePassed) {
  obj.css({backgroundPosition: timePassed+'px 0px'});
}

function season(currentdate){
  var mnth = Math.floor((currentdate.getMonth()-2)/3);
  if (mnth<0){
    return 3;
  }else{
    return mnth;
  }
}

function isNight(currentdate){
  if ((currentdate.getHours()>6) && (currentdate.getHours()<22)){
    return false;
  }else{
    return true;
  };
}
