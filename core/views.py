from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, View

from .forms import UrlForm
from .models import Video, Category
from .service import get_video_info, get_channel_info


class PublishView(FormView):
    template_name = 'core/publish.html'
    form_class = UrlForm

    def get_context_data(self, **kwargs):
        context = super(PublishView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        checkboxes_values = request.POST.getlist('value')
        form = self.get_form()
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            try:
                video = get_video_info(url)
                last_published_video = Video.objects.create(
                    author=video.author, youtube_id=video.video_id,
                    name=video.title, thumbnail=video.medium_thumbnail,
                    description=video.description
                )
                categories = Category.objects.filter(id__in=checkboxes_values)
                for category in categories:
                    last_published_video.categories.add(category)
            except IntegrityError:
                pass

        return redirect('index')


class VideoInfoView(View):

    def post(self, request, *args, **kwargs):
        form = UrlForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('video_url')
            video = get_video_info(url)
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

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context


class VideoView(TemplateView):
    template_name = 'core/videos.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['videos'] = Video.objects.all()
        return context