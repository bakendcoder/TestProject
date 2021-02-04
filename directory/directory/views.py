from django.urls import reverse 
from django.http import HttpResponseRedirect

def dashboard(request):

    return HttpResponseRedirect(reverse("profiles:teachers_list"))