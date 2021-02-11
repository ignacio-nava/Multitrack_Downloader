from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

from home.owner import OwnerListView, OwnerCreateView
from .models import Multitrack, Genre, Band, Fav
from .forms import CreateForm
from .humanize import naturalsize

class MtListView(OwnerListView):
    model = Multitrack
    template_name = 'multitracks/list.html'

    def get(self, request):
        genre_list = Genre.objects.all().order_by('name')
        mt_list = [Multitrack.objects.all().filter(genre__id=g.id).order_by('band') for g in genre_list]
        
        favorites = list()
        if request.user.is_authenticated:
            rows = request.user.favorite_multitracks.values('id')
            favorites = [ row['id'] for row in rows ]

        ctx = {
            'mt_list': mt_list,
            'genre_list': genre_list,
            'favorites': favorites,
        }
        return render(request, self.template_name, ctx)

    def test_func(self):
        return self.request.user.is_staff

class MtCreateView(UserPassesTestMixin, OwnerCreateView):
    model = Multitrack
    template_name = 'multitracks/form.html'
    genre_list = Genre.objects.all().order_by('name')
    band_list = Band.objects.all().order_by('name')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {
            'form': form,
            'genre_list': self.genre_list,
            'band_list': self.band_list,
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {
                'form': form
            }
            return render(request, self.template_name, ctx)

        track = form.save(commit=False)
        track.owner = self.request.user
        preview_type = track.preview.url.split('.')[-1].lower()
        if not preview_type == 'mp3':
            ctx = {
                'form': form,
                'genre_list': self.genre_list,
                'band_list': self.band_list,
                'error_message': 'Preview must be MP3 file'
            }
            return render(request, self.template_name, ctx)
        file_zip_type = track.file_zip.url.split('.')[-1].lower()
        if not file_zip_type == 'zip':
            ctx = {
                'form': form,
                'genre_list': self.genre_list,
                'band_list': self.band_list,
                'error_message': 'Multitrack must be ZIP file'
            }
            return render(request, self.template_name, ctx)
        track.file_size = naturalsize(track.file_zip.size)
        track.save()
        return redirect(self.success_url)

    def test_func(self):
        return self.request.user.is_staff


@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('ADD PK', pk)
        mt = get_object_or_404(Multitrack, id=pk)
        fav = Fav(user=request.user, multitrack=mt)
        try:
            fav.save()
        except IndentationError:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print('DELETE PK', pk)
        mt = get_object_or_404(Multitrack, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, multitrack=mt).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()