 $(document).ready(function(){
  setProgress();
  setInterval('setProgress()', 2000);
  //addJobid();

    $(".starttask").click(function(){
      var ttype = $(this).attr('ttype');

      var url = $(this).attr('href');
      url =  url + "&ttype=" + ttype;
      $.ajax({ type: "GET", url: url});
      if (ttype=="start_task"){
        change_task_button($(this).attr('id'), 'stop');

      }
      else{
        change_task_button($(this).attr('id'), 'start');
      }
      return false;
    });



    $("a[data-toggle=modal]").click(function(){
      var target = $(this).attr('data-target');
      var url = $(this).attr('href');
      var is_task = $(this).attr('is-task');
      if (is_task){
          url = url + $('#select_task').val();
          //alert(url);
      }
      $(target).load(url);
    });




    $("a[data-toggle=pilot]").click(function(){
      var ttype = $(this).attr('ttype');

      var url = $(this).attr('href');
      url =  url + "&ttype=" + ttype;
      $.ajax({ type: "GET", url: url});
      if (ttype=="start_pilot"){
        change_button($(this).attr('id'), 'stop');

      }
      else{
        change_button($(this).attr('id'), 'start');
      }
      return false;
    });

    

    $("a[data-toggle=taskmodal]").click(function(){
      var target = $(this).attr('data-target');
      var url = $(this).attr('href');
      $(target).load(url);
      return false;
    });
      
    $("a[data-toggle=deletetask]").click(function(){
            jConfirm('Message', 'Title', function(confirmed){
                if(confirmed){
                    alert('Delete confirmed');
                }
            });
        });
    });

    //$("#accordion2").collapse('toggle')


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


var setProgress = function() {

  $(".progress-bars").each(function(){
   url = $(this).attr('href') + "&ttype=get_pilot_status";
    $.ajax({
        url: url ,
        success: function(data)
        {
          //console.log(data);
            var msg = $.parseJSON(data);
            var id  = "progress_celery_task_" + msg.ur_id;
            $('#' + id).attr("style", "width: " + msg.percentage + "%");
            $("#status-bar-" + msg.ur_id).text(msg.state);
            //console.log(msg.state);
            if (msg.state=='Stopped'|  msg.state=='Unknown'){
              change_button("celery_task_" + msg.ur_id, 'start');
            }
            else{
              change_button("celery_task_" + msg.ur_id, 'stop');
            }
            //console.log(msg.percentage);

        }
    });
  });

  $(".task-progress-bars").each(function(){
   url = $(this).attr('href') + "&ttype=get_task_status";
    $.ajax({
        url: url ,
        success: function(data)
        {
          //console.log(data);
            var msg = $.parseJSON(data);
            var id  = "progress_task_" + msg.staskid;
            $('#' + id).attr("style", "width: " + msg.percentage + "%");
            $("#status-task-text-" + msg.staskid).text(msg.state);
            console.log(msg.state);
            if (msg.state=='Done' |  msg.state=='Unknown' |  msg.state=='New' ){
              change_task_button("task_action_" + msg.staskid, 'start');
            }
            else{
              change_task_button("task_action_" + msg.staskid, 'stop');
            }
            //console.log(msg.percentage);

        }
    });
  });

};

var addJobid = function() {
  var trail = '?job_id=' +  $(".job_id").val();
  var url = $.url('window.location');
  job_id = url.param('job_id');
};


var change_button = function(element, type) {
//console.log(element + '  '+ type);
  if (type=='stop'){
        $('#' + element).text("Stop Pilot");
        $('#' + element).attr('class', "btn btn-danger");
        $('#' + element).attr('ttype', "stop_pilot");
    }
  else{
        $('#' + element).text("Start Pilot");
        $('#' + element).attr('class', "btn btn-success");
        $('#' + element).attr('ttype', "start_pilot");

  }
};


var change_task_button = function(element, type) {
//console.log(element + '  '+ type);
  if (type=='stop'){
        $('#' + element).text("Stop Task");
        $('#' + element).attr('class', "btn btn-danger");
        $('#' + element).attr('ttype', "stop_task");
    }
  else{
        $('#' + element).text("Start Task");
        $('#' + element).attr('class', "btn btn-success");
        $('#' + element).attr('ttype', "start_task");

  }
};
