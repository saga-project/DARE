show_hide_cores =  function() {
    if ($("#pilotPopupSelect option:selected").attr('type-pilot') =='osg'){
        $('#id_cores').parent().parent().hide();

    } else{
        $('#id_cores').parent().parent().show();
        $('#id_cores').val($("#pilotPopupSelect option:selected").attr('default-cores'));
    }
};
$(document).ready(function() {
  show_hide_cores();

  $('ul.nav a').filter(function() {
      var url = window.location;
        return (this.href == url.href.split( '?' )[0]);
      }).parent().addClass('active');


  $("#pilotPopupSelect").change(function(){
    show_hide_cores();
  });

  var editor = ace.edit("id_pre_script");
  editor.getSession().setMode("ace/mode/python");
  editor.setTheme("ace/theme/textmate");

  $("#runAddTask").click(function() {
    console.log(editor.getValue());
    $("#id_script").val(editor.getValue());
  });

  $("#addTaskForm").validate({
      rules: {
       name : { required : true, minlength: 2 }
      }

  });


  $("#allocatePilotForm").validate({
      rules: {
       walltime : { required : true,  minlength: 1},
       cores : { required : true,  minlength: 1}
      }
  });
  $("#runForm").validate({
      rules: {
       name : { required : true,  minlength: 2}
      }
  });


});