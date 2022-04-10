from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home page"),
    path('folders/<folder>', views.folder_view, name="folder view"),
    path('new/<folder>', views.create_set_view, name="new set"),
    path('makefolder/', views.create_folder_view, name="create folder"),
    path('view/<folder>$<table>-<table_brief>', views.view_set_view,name="view set"),
    path('view/<folder>$<table>-<table_brief>/add', views.add_data_view,name="add to set"),
    path('view/<folder>$<table>-<table_brief>/add_to_archive', views.add_to_archive,name="add to archive"),
    path('archive/<folder>', views.view_archive_view,name="archive view"),
    path('archiveview/<folder>$<table>-<table_brief>', views.view_archiveset_view,name="archive set view"),
    path('favourites/<folder>', views.view_favourites_view, name="favourite view"),
    path('delete/<folder>', views.delete_folder,name="delete folder")
]