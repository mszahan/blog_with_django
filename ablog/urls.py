from django.urls import path
from ablog import views

urlpatterns = [
    path('', views.post_list, name='post_list' ),
    path('tag/<slug:tag_slug>', views.post_list, name='post_by_tag' ),
    path('<int:pk>/<slug:slug>/', views.post_detail, name='post_detail' ),
    path('share/<int:pk>/', views.post_share, name='post_share' ),
    path('search-blog', views.search_blog, name='blog_search' ),
    path('categories', views.category_list, name='cat_list' ),
    path('categories/<str:cat>/', views.category_detail, name='cat_details' ),

]