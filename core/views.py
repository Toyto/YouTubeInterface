from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, View, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.list import MultipleObjectMixin

from .forms import UrlForm
from .models import Video, Category
from . import service


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
                video = service.get_video_info(url)
                last_published_video = Video.objects.create(
                    author=video.author, youtube_id=video.video_id,
                    name=video.title, thumbnail=video.medium_thumbnail,
                    description=video.description, views_count=video.view_count,
                    likes_count=video.likes_count, dislikes_count=video.dislikes_count,
                    rating=service.get_video_rating(video.likes_count, video.dislikes_count)
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
            video = service.get_video_info(url)
            channel_info = service.get_channel_info(video.author.channel_id)
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
        context['categories'] = map(service.get_category_videos, Category.objects.all())
        return context


class VideoView(TemplateView):
    template_name = 'core/videos.html'

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        category = Category.objects.get(id=self.request.GET['id'])
        count = int(self.request.GET['count'])
        context.update(service.get_category_videos(category, count))
        return context