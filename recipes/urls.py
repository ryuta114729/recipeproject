from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('create/', views.recipe_create, name='recipe_create'),
    path('detail/<int:recipe_id>/', views.recipe_detail, name='recipe_detail' ),
    path('review/create/<int:recipe_id>/', views.review_create, name='review_create'),
    path('favorite/<int:recipe_id>/', views.favorite_toggle, name='favorite_toggle'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('mypage/', views.mypage, name='mypage'),
    path('recipe/update/<int:recipe_id>/', views.recipe_update, name='recipe_update'),
    path('recipe/delete/<int:recipe_id>/', views.recipe_delete, name='recipe_delete'),
    path('review/update/<int:review_id>/', views.review_update, name='review_update'),
    path('review/delete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('register/', views.register, name='register'),
]