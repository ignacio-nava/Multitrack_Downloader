import os

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.views import View

from home.owner import OwnerListView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView, OwnerDetailView
from multitracks.models import Multitrack
from .models import Mix, Comment
from .forms import UploadMixForm, CommentForm

class MixListView(OwnerListView):
    model = Mix
    template_name = 'mixes/list.html'
    fail_url = reverse_lazy('mixes:all')

    def get(self, request, slug=None):
        search_tags = {
            'Publish Date': '-created_at',
            'Update Date': '-updated_at',
            'Genre': 'multitrack__genre',
            'Band' : 'multitrack__band',
        }
        if request.user.is_authenticated:
            search_tags.update({'My Mixes': 1})

        if slug != None:
            # Transform the slug into a tag. Example: from 'publish-data' to 'Publish Date'
            slug = ' '.join(slug.split('-')).title()
            if slug in search_tags.keys():
                search_by = slug
            else:   
                return redirect(self.fail_url)
        else:
            search_by = 'Publish Date'

        if type(search_tags[search_by]) == int:
            mixes_list = self.model.objects.filter(owner__id=self.request.user.id).order_by('-created_at')
        else:
            mixes_list = self.model.objects.order_by(search_tags[search_by])

        comments_count_list = []
        for mix in mixes_list:
            comments_by_mix_count = Comment.objects.filter(mix__id=mix.id).count() # How many comments by mix
            comments_count_list.append(comments_by_mix_count)

        ctx = {
            'search_tags': search_tags.keys(),
            'search_by': search_by,
            'mixes_list': zip(mixes_list, comments_count_list),
        }
        return render(request, self.template_name, ctx)

class MixCreateView(OwnerCreateView):
    model = Mix
    template_name = "mixes/form.html"
    success_url = reverse_lazy('mixes:all')
    mt_list = Multitrack.objects.all().order_by('title')

    def get(self, request, pk=None):
        form = UploadMixForm()
        ctx = {
            'form': form,
            'mt_list': self.mt_list,
            }

        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = UploadMixForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {
                'form': form,
                'mt_list': self.mt_list}
            return render(request, self.template_name, ctx)
        mix = form.save(commit=False)
        mix.owner = self.request.user
        mix_type = mix.mix_file.url.split('.')[-1].lower()
        if not mix_type == 'wav':
            ctx = {
                'form': form,
                'mt_list': self.mt_list,
                'error_message': 'Mix must be WAV file'}
            return render(request, self.template_name, ctx)
        mix.save()

        return redirect(self.success_url)

class MixDetailView(OwnerDetailView):
    model = Mix
    template_name = 'mixes/detail.html'

    def get(self, request, pk):
        mix = self.model.objects.get(pk=pk)
        comments_list = Comment.objects.filter(mix__id=mix.id)
        comment_form = CommentForm()
        ctx = {
            'mix': mix,
            'comments_list': comments_list,
            'comment_form': comment_form,
        }

        return render(request, self.template_name, ctx)

class TalkComments(LoginRequiredMixin, View) :
    def get(self, request, pk):
        m = get_object_or_404(Mix, id=pk)
        comments = Comment.objects.filter(mix__id=m.id).order_by('-created_at')
        results = []
        for comment in comments:
            result = [comment.owner.username, naturaltime(comment.created_at), comment.text]
            results.append(result)
        return JsonResponse(results, safe=False)

class MixUpdateView(OwnerUpdateView):
    template_name = 'mixes/form.html'
    success_url = reverse_lazy('mixes:all')
    mt_list = Multitrack.objects.all().order_by('title')

    def get(self, request, pk):
        mix = get_object_or_404(Mix, id=pk, owner=self.request.user)
        form = UploadMixForm(instance=mix)
        ctx = {
            'form': form,
            'mix': mix,
            'mt_list': self.mt_list,
            }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        mix = get_object_or_404(Mix, id=pk, owner=self.request.user)
        old_file = mix.mix_file.path
        form = UploadMixForm(request.POST, request.FILES or None, instance=mix)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        mix = form.save(commit=False)
    
        if not 'mix_file' in form.data.keys():
            mix_type = mix.mix_file.url.split('.')[-1].lower()
            if not mix_type == 'wav':
                ctx = {
                    'form': form,
                    'mt_list': self.mt_list,
                    'error_message': 'Mix must be WAV file'}
                return render(request, self.template_name, ctx)
            os.remove(old_file)
        mix.save()

        # next_url = checkNextUrl(request.get_full_path())
        # if next_url:
        #     return redirect(next_url)
        return redirect(self.success_url)

class MixDeleteView(OwnerDeleteView):
    model = Mix
    success_url = reverse_lazy('mixes:all')

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        m = get_object_or_404(Mix, id=pk)
        comment = Comment(text=request.POST['text'], owner=request.user, mix=m)
        comment.save()

        return redirect(reverse('mixes:mix_detail', args=[m.id]))

class CommentUpdateView(OwnerUpdateView):
    template_name = 'mixes/comment_update.html'

    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk, owner=self.request.user)
        form = CommentForm(instance=comment)

        ctx = {
            'comment': comment,
            'form': form,
        }

        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        comment = get_object_or_404(Comment, id=pk, owner=self.request.user)
        form = CommentForm(request.POST, request.FILES or None, instance=comment)

        if not form.is_valid():
            ctx = {
            'comment': comment,
            'form': form,
            }
            return render(request, self.template_name, ctx)

        comment.save()

        return redirect(reverse('mixes:mix_detail', args=[comment.mix.id]))


class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = 'mixes/comment_confirm_delete.html'

    def get_success_url(self):
        mix = self.object.mix
        return reverse('mixes:mix_detail', args=[mix.id])
