$(document).ready(function(){
            $('#results').hide();
            $('#btn_go').click(function(){
                $.ajax({
                  type: "POST",
                  url: _URLS.video_info,
                  data: $('#url_form').serialize(),
                  dataType: 'json',
                  success: function(json){
                    console.log(json['video_info']);
                    var author = json['video_info']['author'];
                    var title = json['video_info']['title'];
                    var description = json['video_info']['description'];
                    var video_id = json['video_info']['video_id'];
                    var avatar = json['video_info']['avatar'];
                    $('#title').html(title);
                    $('#description').html(description);
                    $('#auth_avatar').html("<img src='" + avatar + "' width='125' height='125'>");
                    $('#author').html(author);
                    $('#player').html(
                        "<iframe id='ytplayer' type='text/html' width='640' height='390' src='http://www.youtube.com/embed/"+ video_id + "' frameborder='0'></iframe>"
                    );
                    $('#results').show('slow');
                    $('.checkbox').checkbox();
                  }
                });
            });
      });