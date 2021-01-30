from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, ListView

from webapp.forms import UserForm
from webapp.models import User, Lesson
from webapp.scraper import parse_site


class UserView(CreateView):
    template_name = 'index.html'
    form_class = UserForm
    model = User

    def get_success_url(self):
        return reverse('parse')

class MyView(View):

    def get(self, request, *args, **kwargs):
        parse = parse_site()
        return redirect('lessons')


class LessonList(ListView):
    model = Lesson
    template_name = 'lesson_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lessons'] = Lesson.objects.all().order_by('pk')
        return context
