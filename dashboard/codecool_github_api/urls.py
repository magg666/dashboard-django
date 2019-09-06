from django.urls import path, include
from rest_framework import routers

from .views import RepositoryView, RepositoryCreate, RepositoryViewSet, TotalStatisticViewSet

router = routers.DefaultRouter()
router.register(r'week', RepositoryViewSet, 'week')
router.register(r'total', TotalStatisticViewSet, 'total')


urlpatterns = [
    path("", RepositoryView.as_view(), name="all_repositories"),
    path("add/", RepositoryCreate.as_view(), name="add_repository"),
    path("repository/", include(router.urls)),

]
