from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.handlelogin, name='root'),
    path('home', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.handlelogin, name="login"),
    path('logout/', views.handlelogout, name="handlelogout"),
    path('articles/', views.article_page, name='article_page'),
    path('user_articles/', views.user_article_page, name='user_article_page'),
    path('add_article/', views.add_article, name='add_article'),
    path('update_article/<int:article_id>/', views.update_article, name='update_article'),
    path('hide_article/<int:article_id>/', views.hide_article, name='hide_article'),
    path('unhide_article/<int:article_id>/', views.unhide_article, name='unhide_article'),
    path('add_comment/<int:article_id>/', views.add_comment, name='add_comment'),
    path('like_article/<int:article_id>/', views.like_article, name='like_article'),
    path('dislike_article/<int:article_id>/', views.dislike_article, name='dislike_article'),
    path('user_list/', views.user_list, name='user_list'),
    path('remove_user/<str:username>/', views.remove_user, name='remove_user'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),

]