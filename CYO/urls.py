from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.create_view, name='create'),
    path('create/<int:ad_index>', views.event_create_view, name='event_create'),
    path('create/choice/<int:event_index>', views.choice_create_view, name='choice_create'),
    path('edit/<int:ad_index>', views.adventure_edit_view, name='ad_edit'),
    path('edit/<int:ad_index>/<int:event_index>', views.event_edit_view, name='ev_edit')
]