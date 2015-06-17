$(document).ready(function(){
              $(".button").click(function(){
                var category_id = $( this ).attr("data-category-id");
                var video_count = $("div[id='video_count']").attr("data-video-count");
                $.ajax({
                  type: "GET",
                  url: _URLS.videos,
                  data: { id: category_id, count: video_count },
                  dataType: "html",
                  success: function(data){
                    $("#" + category_id + "").html(data);
                    $('.rating').rating('disable');
                    if (video_count < 8){
                      $("button[data-category-id=" + category_id + "]").hide();
                    }
                  }
                });
            });
      });