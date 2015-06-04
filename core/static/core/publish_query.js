$(document).ready(function(){
            $('#results').hide();
            $('#player').hide();
            $('#publish').hide();
            $('#checkboxes').hide();
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
                    $('#title').html(title);
                    $('#description').html(description);
                    $('#author').html(author);
                    $('#player').html(
                        "<iframe id='ytplayer' type='text/html' width='640' height='390' src='http://www.youtube.com/embed/"+ video_id + "' frameborder='0'></iframe>"
                    );
                    $('#player').show();
                    $('#results').show('slow');
                    $('#publish').show('slow');
                    $('#checkboxes').show('slow');
                    $('.checkbox').checkbox();
                  }
                });
            });
      });