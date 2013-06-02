
$(document).ready(function() {

  $('ul.nav a').filter(function() {
      var url = window.location;
        return (this.href == url.href.split( '?' )[0]);
      }).parent().addClass('active');

editAreaLoader.init({
  id : "id_script"   // textarea id
  ,syntax: "python"      // syntax to be uses for highgliting
  ,start_highlight: true    // to display with highlight mode on start-up
  ,toolbar: ''
  ,min_width: 525
  ,min_height: 250 
  ,allow_toggle: false
  ,allow_resize: false
  ,replace_tab_by_spaces: true
});




});