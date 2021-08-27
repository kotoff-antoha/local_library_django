from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    # path('', views.index, name='index'),
    # path('books', views.books, name='books'),
    # path('authors', views.authors, name='authors'),
    url(r'^$', views.index, name='index'),
    # url(r'^books$', views.books, name='books'),
    url(r'^books$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    # url(r'^authors$', views.authors, name='authors'),
    url(r'^authors$', views.AuthorListView.as_view(), name='authors'),
    url(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    # url(r'^author/(?P<pk>\d+)$', views.author_info, name='one_author'),
    url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    url(r'^allbooks/$', views.AllBorrowedBooksInLibraryListView.as_view(), name='all-borrowed'),
    url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
    url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    url(r'^book/create/$', views.BookCreate.as_view(), name='book_create'),
    url(r'^book/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
    url(r'^book/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name="book_delete"),
    # url(r'^allbookinstances$', views.AllBookInstancesListView.as_view(), name="all-bookinstances"),
    url(r'^allbookinstances$', views.AllBookInstances, name="all-bookinstances"),
    url(r'^bookinstance/(?P<pk>[-\w]+)$', views.BookInstanceDetailView.as_view(), name='bookinstance-detail'),
    url(r'^bookinstance/create/$', views.BookInstanceCreate.as_view(), name='bookinstance_create'),
    url(r'^bookinstance/(?P<pk>[-\w]+)/update/$', views.BookInstanceUpdate.as_view(), name='bookinstance_update'),
    url(r'^bookinstance/(?P<pk>[-\w]+)/delete/$', views.BookInstanceDelete.as_view(), name='bookinstance_delete'),

]

