from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView
from rest_framework import viewsets

from .forms import RepositoryForm
from .models import Repository, Module
from .serializers import WeekSerializer, TotalSerializer


class RepositoryView(ListView):
    """
    Listed view of all active projects data
    """
    template_name = "codecool_github_api/repository_list.html"
    context_object_name = "current_repositories"

    def get_queryset(self):
        return Repository.current.all()


class RepositoryCreate(View):
    """
    Create view to handle adding data about projects
    """
    template_name = 'codecool_github_api/repository_form.html'
    success_url = reverse_lazy("all_repositories")

    def get(self, request):
        form = RepositoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RepositoryForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Repository.objects.update_or_create(url=data['url'],
                                                defaults={"plan": data['plan'], 'module': data['module']})
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})


# serializers views. Takes into account all modules. Can be transform into not empty modules
class RepositoryViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = WeekSerializer
    http_method_names = ['get']


class TotalStatisticViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = TotalSerializer
    http_method_names = ['get']
