from django.urls import path
from .views import (PostListView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    CategoryListView
                    )
from . import views

app_name = 'post'

urlpatterns = [
    path('post/create/', PostCreateView.as_view(), name='create'),
    path('category/<slug:slug>/', CategoryListView.as_view(),
         name='category'),
    path('search/', views.search_view, name='search'),
    path('', PostListView.as_view(), name='blog-home'),
    path('featured/', views.featured_view, name='featured'),
    path('<slug:slug>/', views.details, name='post-detail'),
    path('<slug:slug>/share', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post-list-by-tag'),
    path('<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),

]
