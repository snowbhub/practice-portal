from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

app_name = "practice"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('jobs-update/<int:id>', JobUpdateView.as_view(), name='jobs-update'),
    # path('job-delete/<int:id>', JobDeleteView.as_view(), name='jobs-delete'),
    path('jobs-delete/<int:id>', JobDeleteView.as_view(), name='jobs-delete'),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('practice', JobListView.as_view(), name='practice'),
    path('practice/<int:id>', JobDetailsView.as_view(), name='practice-detail'),
    path('employer/practice/create', JobCreateView.as_view(), name='employer-practice-create'),
]
