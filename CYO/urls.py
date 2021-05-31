from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create/', views.adventure_create_view, name='create'),
    path('create/<int:ad_index>', views.event_create_view, name='event_create'),
    path('create/choice/<int:event_index>', views.choice_create_view, name='choice_create'),
    path('add/item/<int:ad_index>', views.item_add_view, name='item_add'),
    path('create/item/<int:event_index>', views.event_item_view, name='item_create'),
    path('create/condition/<int:choice_index>', views.choice_item_view, name='condition_create'),
    path('editview/<int:index>', views.adventure_edit_view, name='ad_edit'),
    path('editview/event/<int:index>', views.event_edit_view, name='ev_edit'),
    path('edit/<str:type>/<int:index>', views.generic_edit, name="edit"),
    path('delete/<str:type>/<int:index>/', views.delete_view, name="delete"),
    path('adventure/<int:adventure_index>', views.adventure_view, name='ad_view'),
    path('adventure/event/<int:event_index>', views.adventure_event_view, name='ad_event_view')
]