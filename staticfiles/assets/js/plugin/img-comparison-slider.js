// var divisor = document.getElementById("divisor"),
//   handle = document.getElementById("handle"),
//   slider = document.getElementById("slider");
// function moveDivisor() {
//   handle.style.left = slider.value + "%";
//   divisor.style.width = slider.value + "%";
// }
// window.onload = function () {
//   moveDivisor();
// }; 

!function(g){g.fn.baSlider=function(e){
  var a=g.extend({},g.fn.baSlider.defaults,e),t={},s=this.find("[baSlider-handler]"),i=this.find("[baSlider-image]"),r=this.width(),f=this.height(),n=this.find(".frame"),h=this.find(".after"),o=(this.find(".before"),
  this.find(".after").find("div")),d={elem:null,x:0,y:0,state:!1},l={x:0,y:0},p="auto"==a.width?r:"100%",m="auto"==a.height?f:a.height
  ;return imageDimensions=function(e){var t,i,a=r,s=f,n=s/a,h=e.width(),o=e.height()/h;return o<n?t=(i=s)/o:(i=a*o,t=a),{width:t+"px",height:i+"px",
  left:(a-t)/2+"px",top:(s-i)/2+"px"}},{init:(t={tmpAfterWidth:0,tmpAfterHeight:0,rel:"",init:function(){
  "horizontal"==a.align?(h.width(a.start.horizontal),h.height(m)):(h.width(p),h.height(a.start.vertical)),n.width(r),n.height(m),o.width(r),o.height(m),
  this.tmpAfterWidth=parseInt(h.width()),this.tmpAfterHeight=parseInt(h.height())},handlerPosition:function(e){switch(a.handler.position){case"auto":
  "horizontal"==a.align?(s.css("left",parseInt(h.width())-(s.width()/2+a.handler.offsetX)),
  s.css("top",parseInt(h.height()/2)-(s.height()/2+a.handler.offsetY))):(s.css("left",parseInt(h.width()/2)-(s.width()/2+a.handler.offsetX)),
  s.css("top",parseInt(h.height())-(s.height()/2+a.handler.offsetY)));break;case"top":s.css("left",parseInt(h.width())-(s.width()/2+a.handler.offsetX)),
  s.css("top",parseInt(0+a.handler.offsetY));break;case"bottom":s.css("left",parseInt(h.width())-(s.width()/2+a.handler.offsetX)),
  s.css("bottom",parseInt(0+a.handler.offsetY));break;case"left":s.css("left",parseInt(a.handler.offsetX)),
  s.css("top",parseInt(h.height())-(s.height()/2+a.handler.offsetY));break;case"right":s.css("right",parseInt(a.handler.offsetX)),
  s.css("top",parseInt(h.height())-(s.height()/2+a.handler.offsetY))}},bounce:function(){var t=this
  ;a.anim.play&&(d.state||(this.rel=setTimeout(function(){if("horizontal"==a.align)for(var e=0;e<a.anim.times;e++)h.animate({
  width:"-="+Math.abs(a.anim.distance)},a.anim.speed).animate({width:"+="+Math.abs(a.anim.distance)},a.anim.speed),s.animate({
  left:"-="+Math.abs(a.anim.distance)},a.anim.speed).animate({left:"+="+Math.abs(a.anim.distance)
  },a.anim.speed);else for(e=0;e<a.anim.times;e++)h.animate({height:"-="+Math.abs(a.anim.distance)},a.anim.speed).animate({
  height:"+="+Math.abs(a.anim.distance)},a.anim.speed),s.animate({top:"-="+Math.abs(a.anim.distance)},a.anim.speed).animate({
  top:"+="+Math.abs(a.anim.distance)},a.anim.speed);setTimeout(function(){t.bounce()},a.anim.startDelay)},a.anim.startDelay)))},move:function(e){
  var t=this,i=function(e){if(d.state){d.elem.style.opacity="0.5",l.x=("mousemove"==e.type?e.pageX:e.originalEvent.touches[0].pageX)-d.x,
  l.y=("mousemove"==e.type?e.pageY:e.originalEvent.touches[0].pageY)-d.y;var t=g(d.elem).offset();"horizontal"==a.align?(g(d.elem).offset({
  left:t.left+l.x}),s.css("left",d.x-l.x-h.offset().left-(s.width()/2+a.handler.offsetX))):(g(d.elem).offset({top:t.top+l.y}),
  s.css("top",d.y-l.y-h.offset().top-(s.height()/2+a.handler.offsetY))),
  "horizontal"==a.align?h.width(d.x-l.x-h.offset().left):h.height(d.y-l.y-h.offset().top),
  d.x="mousemove"==e.type?e.pageX:e.originalEvent.touches[0].pageX,d.y="mousemove"==e.type?e.pageY:e.originalEvent.touches[0].pageY}}
  ;g(document).mousemove(function(e){i(e)}),s.on("mouseup mousedown touchstart touchmove touchend",function(e){
  if("mouseup"!=e.type&&"touchend"!=e.type||d.state&&(d.elem.style.opacity="1",d.state=!1,a.reverse&&("horizontal"==a.align?(s.animate({
  left:parseInt(t.tmpAfterWidth)-(s.width()/2+a.handler.offsetX)},a.speed),h.animate({width:parseInt(t.tmpAfterWidth)},a.speed)):(s.animate({
  top:parseInt(t.tmpAfterHeight)-(s.height()/2+a.handler.offsetY)},a.speed),h.animate({height:parseInt(t.tmpAfterHeight)},a.speed))),t.bounce()),
  "mousedown"==e.type||"touchstart"==e.type)return d.state||(d.elem=this,h.clearQueue().stop(),s.clearQueue().stop(),clearTimeout(this.rel),
  this.style.opacity="0.5",d.x="mousedown"==e.type?e.pageX:e.originalEvent.touches[0].pageX,
  d.y="mousedown"==e.type?e.pageY:e.originalEvent.touches[0].pageY,d.state=!0),!1;"touchmove"==e.type&&i(e)})},scaleImages:function(e){
  var t=imageDimensions(i);i.css({width:t.width,height:"auto"==a.imgHeight?t.height:"frame"==a.imgHeight?a.height:a.imgHeight,left:t.left,top:t.top})}
  }).init(),handler:t.handlerPosition(),bounce:t.bounce(),move:t.move(),scaleImages:t.scaleImages()}},g.fn.baSlider.defaults={align:"horizontal",start:{
  horizontal:"50%",vertical:"50%"},anim:{play:!0,startDelay:5e3,delay:1e4,speed:500,distance:15,times:2},handler:{position:"auto",offsetX:0,offsetY:0},
  reverse:!0,speed:300,height:"auto",imgHeight:"auto"}}(jQuery);