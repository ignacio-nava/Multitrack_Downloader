from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse

from home.owner import OwnerListView, OwnerCreateView
from .models import Multitrack
from .forms import CreateForm

class MtListView(OwnerListView):
    model = Multitrack
    template_name = 'multitracks/list.html'

    def get(self, request):
        mt_list = Multitrack.objects.all()
        ctx = {
            'mt_list': mt_list
        }
        return render(request, self.template_name, ctx)

class MtCreateView(OwnerCreateView):
    model = Multitrack
    template_name = 'multitracks/form.html'

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {
            'form': form
        }
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            ctx = {
                'form': form
            }
            return render(request, self.template_name, ctx)

        print(form)

        track = form.save(commit=False)
        track.owner = self.request.user
        track_type = track.preview.url.split('.')[-1].lower()
        if not track_type == 'mp3':
            ctx = {
                'form': form,
                'error_message': 'Audio must be MP3'
            }
            return render(request, self.template_name, ctx)
        #track.content_type = track_type
        track.save()
        return redirect(self.success_url)
        
# def stream_file(request, pk):
#     mt = get_object_or_404(Multitrack, id=pk)
#     response = HttpResponse()
#     response['Content-Type'] = mt.content_type
#     response['Content-Length'] = mt.preview.size
#     response.write(mt.preview)
#     #[print(f'{key} ==> {value}') for key, value in response.__dict__.items()]
#     return response

        


