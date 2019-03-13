from django.urls import path
from . import views

app_name = 'isbn'

urlpatterns = [
    path('', views.BookListView.as_view(), name='book_list'),
    path('word_list/create/', views.SearchWordCreateView.as_view(), name='create'),
    path('word_list/create_done/', views.create_done, name='create_done'),
    path('word_list/',views.WordListView.as_view(), name='word_list'),
    path('word_list/update/<int:pk>/', views.WordUpdateView.as_view(), name='update'),
    path('word_list/update_done/',views.update_done, name='update_done'),
    path('word_list/delete/<int:pk>/', views.WordDeleteView.as_view(), name='delete'),
    path('word_list/delete_done/', views.delete_done, name='delete_done'),
    path('isbn_update/', views.update_isbn_info, name='isbn_update'),
]
