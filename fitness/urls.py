from django.urls import include, path
from . import views
# o '.' significa que importa views da mesma directoria)

app_name = 'fitness'
urlpatterns = [
    # ex: fitness/
    path("", views.index, name='index'),
    # ex: fitness/register
    path('register', views.register_users, name='register_users'),
    # ex: fitness/login
    path('login', views.login_users, name='login_users'),
    # ex: fitness/logout
    path('logout', views.logout_users, name='logout_users'),
    # ex: fitness/account
    path('account', views.user_info, name='user_info'),
    # ex: fitness/account/password
    path('account/password', views.change_password, name='change_password'),
    # ex: fitness/forum
    path('forum', views.forum, name='forum'),
    # ex: fitness/forum
    path('resource_repository', views.resource_repository, name='resource_repository'),
    # ex: fitness/forum/new_Post
    path('forum/new_Post', views.create_post, name='create_post'),
    # ex: fitness/forum/new_Post
    path('resource_repository/new_resource', views.create_resource, name='create_resource'),
    # ex: fitness/forum/11
    path('forum/<int:post_id>', views.post_detalhes, name='post_detalhes'),
    # ex: fitness/forum/11
    path('resource_repository/<int:resource_id>', views.resource_details, name='resource_details'),
    # ex: fitness/forum/11/comment
    path('forum/<int:post_id>/comment', views.create_comentario, name='create_comentario'),
    # ex: fitness/forum/11/comment
    path('resource_repository/<int:resource_id>/create_resource_comment', views.create_resource_comment,
         name='create_resource_comment'),
    path('signup/<int:aula_id>/', views.class_signup, name='class_signup'),
    path('desafios', views.class_page, name='class_page')
]
