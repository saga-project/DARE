 $(document).ready(function(){
   
 //$(".editconf").click(function(event){
 //    alert("Thanks for visiting!");
  // });

$("a[data-toggle=modal]").click(function(){
  var target = $(this).attr('data-target');
  var url = $(this).attr('href');
  $(target).load(url);
});



 });