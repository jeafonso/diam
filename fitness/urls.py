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
    # ex: fitness/forum/new_post
    path('forum/new_post', views.create_post, name='create_post'),
    # ex: fitness/forum/11
    path('forum/<int:post_id>', views.post_detalhes, name='post_detalhes'),
    # ex: fitness/forum/11/comment
    path('forum/<int:post_id>/comment', views.create_comentario, name='create_comentario'),
    # ex: fitness/resource_repository
    path('resource_repository', views.resource_repository, name='resource_repository'),
    # ex: fitness/resource_repository/new_resource
    path('resource_repository/new_resource', views.create_resource, name='create_resource'),
    # ex: fitness/resource_repository/7
    path('resource_repository/<int:resource_id>', views.resource_details, name='resource_details'),
    # ex: fitness/resource_repository/2/create_resource_comment
    path('resource_repository/<int:resource_id>/create_resource_comment', views.create_resource_comment,
         name='create_resource_comment'),
    # ex: fitness/gym_classes
    path('gym_classes', views.class_page, name='class_page'),
    # ex: fitness/gym_classes/4
    path('gym_classes/<int:aula_id>/', views.class_signup, name='class_signup'),
    # ex: fitness/desafios
    path('desafios', views.gym_challenges, name='gym_challenges'),
    # ex: fitness/desafios/new_desafio
    path('desafios/new_desafio', views.create_desafio, name='create_desafio'),
    # ex: fitness/forum
    path('schedule_workout', views.schedule_workout, name='schedule_workout'),
    # ex: fitness/forum/11
    path('schedule_workout/<int:class_id>', views.workout_details, name='workout_details'),
    # ex: fitness/forum
    path('schedule_workout/new_workout', views.create_workout_class, name='create_workout_class'),
]
