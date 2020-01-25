from . import views
from django.urls import path,include
from django.contrib.auth import views as auth_views

app_name = 'blog'
urlpatterns = [
    path("",views.PostList.as_view(),name = 'home'),
    path('create/', views.create_blog, name='create_view'),
    path("<int:id>/",views.post_detail,name = 'post_detail'),
    path("draft/<int:id>/",views.draft_detail,name = 'draft'),
]