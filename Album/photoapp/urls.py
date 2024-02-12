from django.urls import path
from . import views
from .views import HomeView, AlbumDetailView, AlbumCreateView, AlbumUpdateView, AlbumDeleteView, AddPhotoView,UserDetailView,PhotoDetailView,UserAlbumListView
urlpatterns =[
    path('', views.index, name='index'),
    path('home', HomeView.as_view(), name='album-home'),
    path('album/<int:pk>/', AlbumDetailView.as_view(), name='album-detail'),
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<str:username>/albums/', UserAlbumListView.as_view(), name='user_albums'),
    path('photo/<int:pk>/', PhotoDetailView.as_view(), name='photo_detail'),
    path('album/new/', AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/add_photo/', AddPhotoView.as_view(), name='add_photo'),
    path('album/<int:pk>/update/', AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/', AlbumDeleteView.as_view(), name='album-delete'),
    path('about/', views.about, name='album-about'),
    
]