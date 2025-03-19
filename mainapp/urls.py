from django.urls import include, re_path, path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('docs', views.docs, name='docs'),
    path('downloads', views.downloads, name='downloads'),
    re_path(r'^model/(?P<model_id>[0-9]+)$', views.model, name='model'),
    re_path(r'^model/(?P<model_id>[0-9]+)/(?P<revision>[0-9]+)$', views.model, name='model'),
    path('search', views.search, name='search'),
    path('upload', views.upload, name='upload'),
    re_path(r'^revise/(?P<model_id>[0-9]+)$', views.revise, name='revise'),
    re_path(r'^edit/(?P<model_id>[0-9]+)/(?P<revision>[0-9]+)$', views.edit, name='edit'),
    re_path(r'^user/(?P<username>.*)$', views.user, name='user'),
    path('map', views.modelmap, name='map'),
    path('action/editprofile', views.editprofile, name='editprofile'),
    path('action/addcomment', views.addcomment, name='addcomment'),
    path('action/ban', views.ban, name='ban'),
    path('action/hide_model', views.hide_model, name='hide_model'),
    path('action/hide_comment', views.hide_comment, name='hide_comment'),

    re_path(r'^api/info/(?P<model_id>[0-9]+)$', api.get_info, name='get_info'),
    re_path(r'^api/model/(?P<model_id>[0-9]+)/(?P<revision>[0-9]+)$', api.get_model, name='get_model'),
    re_path(r'^api/model/(?P<model_id>[0-9]+)$', api.get_model, name='get_model'),
    re_path(r'^api/filelist/(?P<model_id>[0-9]+)/(?P<revision>[0-9]+)$', api.get_filelist, name='get_list'),
    re_path(r'^api/filelist/(?P<model_id>[0-9]+)$', api.get_filelist, name='get_filelist'),
    re_path(r'^api/file/(?P<model_id>[0-9]+)/(?P<revision>[0-9]+)/(?P<filename>.+)$', api.get_file, name='get_file'),
    re_path(r'^api/filelatest/(?P<model_id>[0-9]+)/(?P<filename>.+)$', api.get_file, name='get_file'),

    re_path(r'^api/tag/(?P<tag>.*)/(?P<page_id>[0-9]+)$', api.lookup_tag, name='lookup_tag'),
    re_path(r'^api/tag/(?P<tag>.*)$', api.lookup_tag, name='lookup_tag'),
    re_path(r'^api/category/(?P<category>.*)/(?P<page_id>[0-9]+)$', api.lookup_category, name='lookup_category'),
    re_path(r'^api/category/(?P<category>.*)$', api.lookup_category, name='lookup_category'),
    re_path(r'^api/author/(?P<username>.*)/(?P<page_id>[0-9]+)$', api.lookup_author, name='lookup_author'),
    re_path(r'^api/author/(?P<username>.*)$', api.lookup_author, name='lookup_author'),

    re_path(r'^api/search/(?P<latitude>-?[0-9]+(\.[0-9]+)?)/(?P<longitude>-?[0-9]+(\.[0-9]+)?)/(?P<distance>[0-9]+(\.[0-9]+)?)/(?P<page_id>[0-9]+)$', api.search_range, name='lookup_range'),
    re_path(r'^api/search/(?P<latitude>-?[0-9]+(\.[0-9]+)?)/(?P<longitude>-?[0-9]+(\.[0-9]+)?)/(?P<distance>[0-9]+(\.[0-9]+)?)$', api.search_range, name='lookup_range'),
    re_path(r'^api/search/title/(?P<title>.*)/(?P<page_id>[0-9]+)$', api.search_title, name='search_title'),
    re_path(r'^api/search/title/(?P<title>.*)$', api.search_title, name='search_title'),
    path('api/search/full', api.search_full, name='search_full'),
]
