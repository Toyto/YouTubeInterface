from django.shortcuts import render, redirect
from .forms import UrlForm
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from .service import get_video_info, VideoInfo, get_channel_info, ChannelInfo
from django.views.generic import RedirectView, TemplateView, FormView, View
from .models import Video, Category


class PublishView(FormView):
    template_name = 'core/publish.html'
    form_class = UrlForm

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        checkboxes_values = request.POST.getlist('value')
        last_published_video = Video.objects.last()
        categories = Category.objects.filter(id__in=checkboxes_values)
        for category in categories:
            last_published_video.categories.add(category)

        return redirect('index')


class VideoInfoView(View):

    def post(self, request, *args, **kwargs):
        form = UrlForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            video = get_video_info(url)
            Video.objects.create(
                author=video.author, youtube_id=video.video_id
            )
            channel_info = get_channel_info(video.author.channel_id)
            return JsonResponse({
                'video_info': {
                    'title': video.title,
                    'description': video.description,
                    'video_id': video.video_id,
                    'author': video.author.name,
                    'avatar': channel_info.medium_thumbnail
                }
            })
        else:
            return HttpResponseBadRequest()


class IndexView(TemplateView):
    template_name = 'core/index.html'
