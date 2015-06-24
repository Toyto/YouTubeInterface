$(document).ready(function(){
  function encodeQueryData(data) {
     var ret = [];
     for (var d in data)
        ret.push(encodeURIComponent(d) + "=" + encodeURIComponent(data[d]));
     return '?' + ret.join("&");
  }

  $('.special.cards .image').dimmer({on: 'hover'});
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
          parent.find('.rating').rating('disable');
          parent.find('.special.cards .image').dimmer({on: 'hover'});
        }
      });
  });

  $("body").on("click", ".card .dimmable.image", function(){
    var video_id = $(this).attr("data-video-id");
    var oembed_url = (
      'http://www.youtube.com/embed/' +
      video_id +
      encodeQueryData({
        autoplay: 1,
        enablejsapi: 1,
        hq: 1,
      })
    )
    $('#modal' + video_id + ' iframe').attr('src', oembed_url);
    $("#modal" + video_id).modal("setting", {
      onHidden: function () {
        $(this).find('iframe').attr('src', '');
      }
    }).modal("show");
  });
});
