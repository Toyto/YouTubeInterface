$(document).ready(function(){
  $('.rating').rating('disable');
  $(".category-block").on("click", ".show-more-btn", function(event){
      var button = $(event.target);
      var category_id = button.attr("data-category-id");
      var video_count = parseInt(button.attr("data-video-count"));
      $.ajax({
        type: "GET",
        url: _URLS.videos,
        data: { id: category_id, count: video_count + 4 },
        dataType: "html",
        success: function(data){
          var container = button.closest('.category-block');
          var parent = container.parent();
          container.replaceWith(data);
          $(parent).find('.rating').rating('disable');
        }
      });
  });
});
