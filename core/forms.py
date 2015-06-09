from django import forms


class UrlForm(forms.Form):
    video_url = forms.URLField(label='video url', max_length=200)

