from django.views.generic import TemplateView

class MainPageView(TemplateView):
    template_name = 'angular/main_page.html'
