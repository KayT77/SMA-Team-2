from django.urls import path 
from Accounts import views as accountViews
from. import views

# app_name = "details"

urlpatterns = [
    path("create_post/", views.create_post, name="create_post"),
    path("update_post/<int:id>/", views.update_post, name="update_post"),
    path("delete_post/<int:id>/", views.delete_post, name="delete_post"),
    path('like_post/<post_id>/', views.like_post, name='like_post'),
    path('unlike_post/<post_id>/', views.unlike_post, name='unlike_post'),
    path('search_post/', views.search_post, name='search_post'),

    # Mock URLs.
    path('view_posts_mock/', views.view_posts_mock, name='view_posts_mock'),
    path('view_posts_mock/<post_id>/', views.view_post_mock, name='view_post_mock'),
]
