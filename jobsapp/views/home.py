from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from jobsapp.forms import ApplyJobForm, AboutForm
from jobsapp.models import Job, Applicant, About


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'practice'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        return context


class SearchView(ListView):
    model = Job
    template_name = 'practice/search.html'
    context_object_name = 'practice'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])


class JobListView(ListView):
    model = Job
    template_name = 'practice/jobs.html'
    context_object_name = 'practice'
    paginate_by = 5


class JobDetailsView(DetailView):
    model = Job
    template_name = 'practice/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Practice doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try: 
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Practice doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the practice!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('practice:home'))

    def get_success_url(self):
        return reverse_lazy('practice:practice-detail', kwargs={'id': self.kwargs['job_id']})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this practice')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class AboutView(CreateView):
    model = About
    template_name = 'about.html'
    form_class = AboutForm

    def get_context_data(self, **kwargs):
        
        return super().get_context_data(**kwargs)
        context['about_page'] = 'active'
        return context


    def get(self, request, *args, **kwargs):
        context = {'form': AboutForm()}
        return render(request, 'about.html', context)
    
    def post(self, request, *args, **kwargs):
        form = AboutForm(request.POST)

        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()
            messages.success(request, 'Sent message to the admin successfully')
            return HttpResponseRedirect(reverse_lazy('practice:about'))
        return render(request, 'about.html', {'form': form})

class JobDeleteView(DeleteView):
    model = Job
    template_name = 'practice/delete.html'
    #pk_url_kwarg = 'id'

    # def get_object(self, queryset=None):
    #     id = self.kwargs.get("id")
    #     return get_object_or_404(Job,id=id)

    def get_object(self, queryset=None):
        id = self.kwargs.get("id")
        obj= get_object_or_404(Job,id=id)
        if obj is None:
            raise Http404("Job doesn't exists")
        elif obj.user == self.request.user:
            return obj
        else:
            raise PermissionDenied


    def get_success_url(self):
        return reverse_lazy('practice:employer-dashboard')
