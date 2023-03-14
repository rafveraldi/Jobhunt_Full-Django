from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


from django.urls import reverse_lazy

from .models import Job


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = ['job_title', 'company', 'url',
              'date_applied', 'stage', 'notes']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('jobs')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    sucess_url = reverse_lazy('jobs')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('jobs')
        return super(RegisterPage, self).get(*args, **kwargs)


class JobList(LoginRequiredMixin, ListView):
    model = Job
    context_object_name = 'jobs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = context['jobs'].filter(user=self.request.user)
        context['count'] = context['jobs'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['jobs'] = context['jobs'].filter(
                job_title__icontains=search_input)

        context['search-input'] = search_input
        return context


class JobDetail(LoginRequiredMixin, DetailView):
    model = Job
    context_object_name = 'job'
    template_name = 'base/job.html'


class JobCreate(LoginRequiredMixin, CreateView):
    model = Job
    fields = ['job_title', 'company', 'url',
              'date_applied', 'stage', 'notes']
    success_url = reverse_lazy('jobs')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(JobCreate, self).form_valid(form)


class JobUpdate(LoginRequiredMixin, UpdateView):
    model = Job
    fields = ['job_title', 'company', 'url',
              'date_applied', 'stage', 'notes']
    success_url = reverse_lazy('jobs')


class JobDelete(LoginRequiredMixin, DeleteView):
    model = Job
    context_object_name = 'job'
    success_url = reverse_lazy('jobs')
