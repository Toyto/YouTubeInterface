$(document).ready(function(){
  $('.rating').rating('disable');
  $(".more_videos").on("click", "button", function(){
      var category_id = $( this ).attr("data-category-id");
      var video_count = parseInt($("#btn_for_category" + category_id).attr("data-video-count"));
      $.ajax({
        type: "GET",
        url: _URLS.videos,
        data: { id: category_id, count: video_count + 4 },
        dataType: "html",
        success: function(data){
          console.log(data);
          $("." + category_id + "").replaceWith(data);
          $('.rating').rating('disable');
        }
      });
  });
});