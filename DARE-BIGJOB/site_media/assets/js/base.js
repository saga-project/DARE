
$(document).ready(function() {

  $('ul.nav a').filter(function() {
      var url = window.location;
        return (this.href == url.href.split( '?' )[0]);
      }).parent().addClass('active');

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

});