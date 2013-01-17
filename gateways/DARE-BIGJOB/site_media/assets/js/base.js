 $(document).ready(function(){
   

$("a[data-toggle=modal]").click(function(){
  var target = $(this).attr('data-target');
  var url = $(this).attr('href');
  $(target).load(url);
  var checkme = $(this).attr('checkme');
  $("#" + checkme).attr('checked', true);

});


$("a[data-toggle=taskmodal]").click(function(){
  var target = $(this).attr('data-target');
  var url = $(this).attr('href');
  $(target).load(url);
  return false;
});
  

 });