$(document).ready(function(){
                $.ajax({
                  type: "GET",
                  url: _URLS.video_info,
                  dataType: 'html',
                  success: function(data){
                    $('#videos').html(data);
                    console.log(data);
                    $('#more').click(function(){
                      });
                  }
            });
      });