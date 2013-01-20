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
      
    $("a[data-toggle=deletetask]").click(function(){
      alert(hi);
            jConfirm('Message', 'Title', function(confirmed){
                if(confirmed){
                    alert('Delete confirmed');
                }
            });
        });
    });


    var opts = {
      lines: 15, // The number of lines to draw
      length: 21, // The length of each line
      width: 5, // The line thickness
      radius: 25, // The radius of the inner circle
      corners: 1, // Corner roundness (0..1)
      rotate: 83, // The rotation offset
      color: '#000', // #rgb or #rrggbb
      speed: 2.1, // Rounds per second
      trail: 85, // Afterglow percentage
      shadow: false, // Whether to render a shadow
      hwaccel: false, // Whether to use hardware acceleration
      className: 'spinner', // The CSS class to assign to the spinner
      zIndex: 2e9, // The z-index (defaults to 2000000000)
      top: 'auto', // Top position relative to parent in px
      left: 'auto' // Left position relative to parent in px
};
