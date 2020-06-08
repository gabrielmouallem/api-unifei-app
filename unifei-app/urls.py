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
from authentication.views import LoginView, CreateUserView
from markers.views import GenericMarkerModelView, EventMarkerModelView, ConstructionMarkerModelView, \
    StudyGroupMarkerModelView, ExtraActivityMarkerModelView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', LoginView.as_view(), name='auth'),
    path('auth/register/', CreateUserView.as_view(), name='create-user'),

    path('GenericMarker/create/', GenericMarkerModelView.as_view(), name='generic-marker-create'),
    path('EventMarker/create/', EventMarkerModelView.as_view(), name='event-marker-create'),
    path('ConstructionMarker/create/', ConstructionMarkerModelView.as_view(), name='construction-marker-create'),
    path('StudyGroupMarker/create/', StudyGroupMarkerModelView.as_view(), name='study-group-marker-create'),
    path('ExtraActivityMarker/create/', ExtraActivityMarkerModelView.as_view(), name='extra-activity-marker-create'),
]
