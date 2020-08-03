from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('home/', views.homePage, name='person_changelist'),
    path('logout/', views.logoutUser, name='logout'),
    #path('add/', views.PersonCreateView.as_view(), name='person_add'),
    #path('<int:pk>/', views.PersonUpdateView.as_view(), name='person_change'),
    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'),
    path('ajax/load-vanues/', views.load_vanues, name='ajax_load_vanues'),
    path('ajax/load-data/', views.load_data, name='ajax_load_data'),
]
 