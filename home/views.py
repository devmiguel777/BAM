from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.views.generic import TemplateView

from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import MetaTag, MetaTagCompany, Page
from django.views import View
from django.http import HttpResponse


class BaseView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, self.get_context_data())

    def get_context_data(self, **kwargs):
        context = {}
        slug = self.request.path
        page, created = Page.objects.get_or_create(slug=slug)
        if created:
            page.title = 'New Page'
            page.content = 'This is a new page.'
            page.save()
        context['metatags'] = page.meta_tags    
        return context



class HomePageView(BaseView):
    template_name = 'home/home.html'
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

