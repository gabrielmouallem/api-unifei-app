"""unifei-app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from authentication.views import LoginView, CreateUserView, CreateProfileView, SelectedProfileView, UpdateProfileView
from markers.views import ListAllMarkersView, ExtraActivityMarkerCreateView, StudyGroupMarkerCreateView, \
    ConstructionMarkerCreateView, EventMarkerCreateView, GenericMarkerCreateView, GenericMarkerDestroyView, \
 \
    SelectedMarkerView, GenericMarkerUpdateView, EventMarkerUpdateView, ConstructionMarkerUpdateView, \
    StudyGroupMarkerUpdateView, ExtraActivityMarkerUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', LoginView.as_view(), name='auth'),
    path('auth/register/', CreateUserView.as_view(), name='create-user'),

    path('profile/', SelectedProfileView.as_view(), name='profile'),
    path('profile/create/', CreateProfileView.as_view(), name='create-profile'),
    path('profile/<pk>/edit/', UpdateProfileView.as_view(), name='edit-profile'),

    path('markers/', ListAllMarkersView.as_view(), name='markers-list'),

    path('markers/<pk>/', SelectedMarkerView.as_view(), name='selected-marker'),

    path('GenericMarker/create/', GenericMarkerCreateView.as_view(), name='generic-marker-create'),
    path('EventMarker/create/', EventMarkerCreateView.as_view(), name='event-marker-create'),
    path('ConstructionMarker/create/', ConstructionMarkerCreateView.as_view(), name='construction-marker-create'),
    path('StudyGroupMarker/create/', StudyGroupMarkerCreateView.as_view(), name='study-group-marker-create'),
    path('ExtraActivityMarker/create/', ExtraActivityMarkerCreateView.as_view(), name='extra-activity-marker-create'),

    path('GenericMarker/<pk>/update/', GenericMarkerUpdateView.as_view(), name='generic-marker-update'),
    path('EventMarker/<pk>/update/', EventMarkerUpdateView.as_view(), name='event-marker-update'),
    path('ConstructionMarker/<pk>/update/', ConstructionMarkerUpdateView.as_view(), name='construction-marker-update'),
    path('StudyGroupMarker/<pk>/update/', StudyGroupMarkerUpdateView.as_view(), name='study-group-marker-update'),
    path('ExtraActivityMarker/<pk>/update/', ExtraActivityMarkerUpdateView.as_view(), name='extra-activity-marker-update'),

    path('GenericMarker/<pk>/delete/', GenericMarkerDestroyView.as_view(), name='generic-marker-delete'),
]
