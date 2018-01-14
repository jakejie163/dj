from django.urls import path

from . import views

urlpatterns = [
    path('publishers/', views.PublisherList.as_view(), name='publisher-list'),
    path('publishers/<int:pk>/', views.PublisherDetail.as_view(), name='publisher-detail'),
    
    path('books/', views.BookList.as_view(), name='book-list'),
    path('books/<publisher>/', 
        views.PublisherBookList.as_view, 
        name='publisher-book-list'),
    
    path('authors/',
        views.AuthorList.as_view(),
        name='author-list'),

    path('authors/<int:pk>/', 
        views.AuthorDetailView.as_view(), 
        name='author-detail'),

    path('author/add/',
        views.AuthorCreate.as_view(),
        name='author-add'),

    path('author/<int:pk>/',
        views.AuthorUpdate.as_view(),
        name='author-update'),

    path('author/<int:pk>/delete/',
        views.AuthorDelete.as_view(),
        name='author-delete'),

    #path('contact/', views.contact, name='contact'),
    path('contact/', 
        views.ContactView.as_view(), 
        name='contact'),
    path('pdf/', views.pdf_view, name='pdf'),

]
