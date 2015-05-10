function wind(obj, speed){
  var start = Date.now(); // сохранить время начала
  var fps = 50; // 50 кадров в секунду
  // var timer = setInterval(function() {
  //   if (время вышло) clearInterval(timer);
  //   else немного увеличить left
  // }, 1000 / fps)
  var timer = setInterval(function() {
    // вычислить сколько времени прошло с начала анимации
    var timePassed = Date.now() - start;

    // if (timePassed >= 2000) {
    //   clearInterval(timer); // конец через 2 секунды
    //   return;
    // }

    // рисует состояние анимации, соответствующее времени timePassed
    draw(obj,timePassed*speed);
  }, 20);
  obj.css({backgroundPosition: '200px 0px'});
}

// в то время как timePassed идёт от 0 до 2000
// left принимает значения от 0 до 400px
function draw(obj,timePassed) {
  obj.css({backgroundPosition: timePassed+'px 0px'});
}