from django.shortcuts import render
from django.views import View

from .models import Multitrack

class MtListView(View):
    model = Multitrack
    template_name = 'multitracks/list.html'

    def get(self, request):
        mt_list = Multitrack.objects.all()
        ctx = {'mt_list': mt_list}
        return render(request, self.template_name, ctx)
