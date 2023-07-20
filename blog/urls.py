from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    # post views
    path('list/', views.post_list, name='post_list'),
    re_path(r'^tag/(?P<tag_slug>[\w]+)/$', views.post_list, name='post_list_by_tag'),
    path('', views.PostListView.as_view(), name='post_lists'),
    # path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='post_lists_by_tag'),
    re_path(r'^tag/(?P<tag_slug>[\w]+)/$', views.PostListView.as_view(), name='post_lists_by_tag'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<post>[\w]+)/$',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]