from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
  path('', ShowAllProfilesView.as_view(), name="show_all"),
  path('profile/<int:pk>', ShowProfilePageView.as_view(), name="show_profile"),
  path('create_profile', CreateProfileView.as_view(), name='create_profile'),
  path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name='create_status'),
  
]