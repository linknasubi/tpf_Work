from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('home/', views.homePage, name='person_changelist'),
    path('download/', views.csvExport, name='downloadCSV'),
    path('logout/', views.logoutUser, name='logout'),

] 
 