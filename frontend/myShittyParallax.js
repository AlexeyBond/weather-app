// следит за объектом и сдвигает его фон
function wind(obj, speed){
  var start = Date.now();
  var timer = setInterval(function() {
    var timePassed = (Date.now() - start)*speed;
    obj.css({backgroundPosition: timePassed+'px 0px'});
  }, 50);
  obj.css({backgroundPosition: '200px 0px'});
}
// принимает дату, возвращает magic number. 0-весна, 1-лето, 2-осень, 3-зима
function season(currentdate){
  var mnth = Math.floor((currentdate.getMonth()-2)/3);
  if (mnth<0){
    return 3;
  }else{
    return mnth;
  }
}
// принимает дату, возвращает true если ночь
function isNight(currentdate){
  if ((currentdate.getHours()>6) && (currentdate.getHours()<22)){
    return false;
  }else{
    return true;
  };
}
