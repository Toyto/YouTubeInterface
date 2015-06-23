$(document).ready(function(){
  $('.special.cards .image').dimmer({
    on: 'hover'
    });
  $('.rating').rating('disable');
  $("body").on("click", ".show-more-btn", function(event){
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
          $(parent).find('.special.cards .image').dimmer({
            on: 'hover'
            });
        }
      });
  });
  $("body").on("click", ".card .dimmable.image", function(event){
    var video_id = $(this).attr("id");
    $('#ytplayer_for'+video_id).replaceWith(
              "<iframe id='ytplayer' type='text/html' width='100%' height='500px' src='http://www.youtube.com/embed/"+ video_id + "?autoplay=1&enablejsapi=1&vq=hd720' frameborder='0'></iframe>"
          );
    $("#modal"+video_id).modal("setting", {
        onHidden: function () {
          $('.modal.transition').remove();
        }
    }).modal("show");
  });
});
