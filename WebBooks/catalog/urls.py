from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import re_path as url

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-books'),
    url(r'^author_add/$', views.authors_add, name='authoradd'),
    url(r'^create/$', views.create),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    path('edit1/<int:id>/', views.edit1, name='edit1'),
    url(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/update/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/delete/(?P<pk>\d+)$', views.BookUpdate.as_view(), name='book_delete'),
    url(r'^register/$', views.register, name='register'),
    url(r'^status_books/$', views.book_status.as_view(), name='status_book'),
    path('edit/<int:pk>/', views.edit_field, name='edit_field'),
    path('<int:book_id>/purchase/', views.purchase, name='purchase'),
    path('<int:book_id>/download/', views.download, name='download'),
    ]