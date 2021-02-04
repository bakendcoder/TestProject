from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import TeacherSearchForm, TeacherProfileBulkCreateForm
from .models import TeacherProfile
from .teacher import Teacher


class TeacherListView(ListView):
    model = TeacherProfile
    template_name = "profiles/teacher_list.html"
    form_class = TeacherSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(self.request.GET)
        return context

    def get_queryset(self):
        tobj = Teacher()
        qs = tobj.queryset(self.request)
        return qs

class TeacherDetailView(DetailView):
    
    template_name = "profiles/teacher_detail.html"
    model = TeacherProfile
    context_object_name = "teacher_obj"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Teacher Details"
        return context

class TeacherBulkCreateView(LoginRequiredMixin, View):
    
    template_name = "profiles/teacher_create_bulk.html"
    form_class = TeacherProfileBulkCreateForm

    def get(self, request):
        context = {}
        context["form"] = TeacherProfileBulkCreateForm
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        csv_errors = {}
        if form.is_valid():
            obj, csv_errors = form.save()
            if not csv_errors["exists"]:
                messages.success(request, 'Teacher Profile is successfully created')
                return HttpResponseRedirect(self.get_success_url())
        
        context = {}
        if csv_errors["success_objs"]:
            messages.warning(request, 'Some of the Teacher profiles are not created.')
        else:
            messages.error(request, 'Some errors occured while creating teachers profile')
        context["csv_errors"] = csv_errors
        context["form"] = form
        return render(request, self.template_name, context)

    
    def get_success_url(self):
        return reverse("profiles:teachers_list")