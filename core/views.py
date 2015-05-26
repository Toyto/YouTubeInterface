from django.shortcuts import render
from .forms import UrlForm
from django.http import JsonResponse, HttpResponse
from .service import get_video_info, VideoInfo
from django.views.generic import View, TemplateView, FormView


class IndexView(TemplateView):
    template_name = 'core/index.html'


class PublishView(FormView):

    template_name = 'core/publish.html'
    form_class = UrlForm
    success_url = 'publish/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            video = get_video_info(url)
            return JsonResponse({
                'video_info': {
                    'title': video.title,
                    'description': video.description,
                    'video_id' : video.video_id,
                    'author': video.author.name
                }
            })
