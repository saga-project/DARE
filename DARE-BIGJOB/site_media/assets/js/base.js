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

  editAreaLoader.init({
    id : "id_script",
    syntax: "python",
    start_highlight: true,
    toolbar: '',
    min_width: 525,
    min_height: 250,
    allow_toggle: false,
    allow_resize: false,
    replace_tab_by_spaces: true
  });

  $("#runFormSubmit").click(function(){
    $("#id_script").val(editAreaLoader.getValue("id_script"));
  });

  $("#addTaskForm").validate({
      rules: {
       name : { required : true, minlength: 2 },
       script : { required : true, minlength: 30 }
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