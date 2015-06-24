$(document).ready(function(){
  $('.ui.checkbox').checkbox();

  $('#publish_button').click(function(){
    $('#input_url').val($('#id_video_url').val());
    $('#submit-form').submit();
  });

  $('#btn_go').click(function(){
      $.ajax({
        type: "POST",
        url: _URLS.video_info,
        data: $('#url_form').serialize(),
        dataType: 'json',
        success: function(json){
          var author = json['video_info']['author'];
          var title = json['video_info']['title'];
          var description = json['video_info']['description'];
          var video_id = json['video_info']['video_id'];
          var avatar = json['video_info']['avatar'];

          $.each(description.split('\n'), function(i, line) {
            $('#description').append($('<p/>', {html: line}));
          });
          $('#title').text(title);
          $('#author_avatar').attr('src', avatar)
          $('#author').text(author);
          $('#video-block').html(
              "<iframe id='ytplayer' type='text/html' width='640' height='390' src='http://www.youtube.com/embed/"+ video_id + "' frameborder='0'></iframe>"
          );
          $('.step2').show();
          $('#step-add-video').removeClass('active').addClass('completed');
          $('#step-select-categories').removeClass('disabled').addClass('active');
          $('html, body').animate({
            scrollTop: $("#video-block").offset().top
          }, 100);
        }
      });
  });
});

