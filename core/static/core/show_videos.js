$(document).ready(function(){
  $(".more_videos").on("click", "button", function(event){
      console.log(event);
      var category_id = $( this ).attr("data-category-id");
      var video_count = parseInt($("#btn_for_category" + category_id).attr("data-video-count"));
      $.ajax({
        type: "GET",
        url: _URLS.videos,
        data: { id: category_id, count: video_count + 4 },
        dataType: "html",
        success: function(data){
          $("#" + category_id + "").html(data);
          $('.rating').rating('disable');
        }
      });
  });
});