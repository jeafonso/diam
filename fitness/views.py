import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.defaultfilters import register
from django.urls import reverse
from django.utils import timezone
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage


# A ser usado no decorator @user_passes_test, testar se é um funcionário ou superuser
def admin_check(request, user):
    return user.is_authenticated and (user.is_superuser or request.session.get('funcionario_id') is not None)


def index(request):
    context = {}
    utilizador = None

    # Se estiver logado
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    if utilizador:
        context = {'utilizador': utilizador}
    return render(request, 'fitness/index.html', context)


def schedule_workout(request):
    utilizador = None
    cliente = None

    # Se estiver logado e for cliente
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    # Se estiver logado e for funcionário
    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = json.loads(request.body)
        inputValue = data.get('inputValue', '')

        workout = Aula.objects.filter(name=inputValue)
        aula = workout[0]
        addition = aula.attendees.add(cliente)
        aula.save()

    monday_classes = Aula.objects.filter(day='Monday')
    tuesday_classes = Aula.objects.filter(day='Tuesday')
    wednesday_classes = Aula.objects.filter(day='Wednesday')
    thursday_classes = Aula.objects.filter(day='Thursday')
    friday_classes = Aula.objects.filter(day='Friday')
    saturday_classes = Aula.objects.filter(day='Saturday')

    starting_times = STARTING_TIMES
    week_days = WEEK_DAYS
    instructors = Funcionario.objects.all()

    hours = [time[0] for time in STARTING_TIMES]

    context = {'monday_classes': monday_classes, 'tuesday_classes': tuesday_classes,
               'wednesday_classes': wednesday_classes, 'thursday_classes': thursday_classes,
               'friday_classes': friday_classes, 'saturday_classes': saturday_classes,
               'starting_times': starting_times,
               'week_days': week_days, 'instructors': instructors, 'hours': hours}

    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/schedule_workout.html', context)


@register.filter(name='times')
def times(start, end):
    return range(start, end)


def forum(request):
    utilizador = None

    # Se estiver logado e for cliente
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    # Se estiver logado e for funcionário
    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    forum_post_list = Post.objects.order_by('-pub_data')

    # Paginar a lista de posts.
    paginator = Paginator(forum_post_list, 3)  # 3 posts por página
    page_number = request.GET.get('page')  # Número da página atual

    try:
        # Retrieve the forum posts for the requested page
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        page_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        page_posts = paginator.page(paginator.num_pages)

    context = {'page_posts': page_posts}
    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/forum.html', context)


def resource_repository(request):
    utilizador = None

    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    resource_repository_list = Resource.objects.order_by('-pub_data')[:10]
    resource_types = TypesOfResource.choices()

    context = {'resource_repository_list': resource_repository_list, 'resource_types': resource_types}

    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/resource_repository.html', context)

@login_required
def gym_challenges(request):
    utilizador = None

    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    gym_desafio_list = Desafio.objects.order_by('-data_inicio')
    desafio_types = TypesOfDesafio.choices()
    desafios_enlisted = {}

    context = {'gym_desafio_list': gym_desafio_list, 'desafio_types': desafio_types}
    if utilizador:
        if request.method == 'POST' and request.POST:
            desafio_id = request.POST['desafio_id']
            desafio = get_object_or_404(Desafio, pk=desafio_id)
            desafio.participantes.add(utilizador)

        context['utilizador'] = utilizador

    return render(request, 'fitness/desafios.html', context)


def post_detalhes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    utilizador = None

    # Se estiver logado e for cliente
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    # Se estiver logado e for funcionário
    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    context = {'post': post}
    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/post_detalhes.html', context)


def resource_details(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)
    utilizador = None

    # Se estiver logado e for cliente
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    # Se estiver logado e for funcionário
    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    context = {'resource': resource}
    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/resource_detail.html', context)


def workout_details(request, class_id):
    workout = get_object_or_404(Aula, pk=class_id)
    utilizador = None

    # Se estiver logado e for cliente
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = get_object_or_404(Utilizador, user_id=cliente.utilizador.user.id)

    # Se estiver logado e for funcionário
    if request.session.get('funcionario_id') is not None:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = get_object_or_404(Utilizador, user_id=funcionario.utilizador.user.id)

    context = {'workout': workout}
    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/workout_details.html', context)


@login_required
def create_post(request):
    if request.method == 'POST' and request.POST:
        # Guardar o post
        titulo = request.POST['post_titulo']
        descricao = request.POST['post_descricao']
        autor = get_object_or_404(Utilizador, user=request.user)

        post = Post(autor=autor, titulo=titulo, descricao=descricao, pub_data=timezone.now())
        post.save()
        return HttpResponseRedirect(reverse('fitness:forum'))


@login_required
def create_resource(request):
    if request.method == 'POST' and request.POST:
        title = request.POST['resource_title']
        description = request.POST['resource_description']
        author = get_object_or_404(Utilizador, user=request.user)
        resource_type = request.POST['resource_type']

        resource = Resource(author=author, title=title, description=description, type=resource_type,
                            pub_data=timezone.now())
        resource.save()

        return HttpResponseRedirect(reverse('fitness:resource_repository'))

#@user_passes_test(admin_check)
def create_desafio(request):
    if request.method == 'POST' and request.POST:
        nome = request.POST['desafio_nome']
        type = request.POST['desafio_type']
        descricao = request.POST['desafio_descricao']
        data_inicio = request.POST['desafio_data_inicio']
        data_fim = request.POST['desafio_data_fim']
        regras = request.POST['desafio_regras']

        desafio = Desafio(nome=nome, type=type, descricao=descricao, data_inicio=data_inicio,
                          data_fim=data_fim, regras=regras)
        desafio.save()

        return HttpResponseRedirect(reverse('fitness:gym_challenges'))


@login_required
def create_workout_class(request):
    if request.method == 'POST' and request.POST:

        name = request.POST['class_name']
        description = request.POST['class_description']

        instructor_pk = request.POST.get('instructor')
        instructor = get_object_or_404(Funcionario, id=instructor_pk)

        starting_time = request.POST['starting_time']
        week_day = request.POST['week_day']
        max_attendees = request.POST['max_attendees']

        workout_class = Aula(name=name, description=description, instructor=instructor, start_time=starting_time,
                             day=week_day, max_attendees=max_attendees)
        workout_class.save()

        return HttpResponseRedirect(reverse('fitness:schedule_workout'))


@login_required
def create_comentario(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.POST:
        texto_comentario = request.POST['comment_texto']
        autor = get_object_or_404(Utilizador, user=request.user)

        novo_comentario = post.comentario_set.create(autor=autor, texto=texto_comentario, pub_data=timezone.now())
        return HttpResponseRedirect(reverse('fitness:post_detalhes', args=(post.id,)))


@login_required
def create_resource_comment(request, resource_id):
    resource = get_object_or_404(Resource, pk=resource_id)

    if request.method == 'POST' and request.POST:
        comment_text = request.POST['comment_texto']
        author = get_object_or_404(Utilizador, user=request.user)

        new_comment = resource.commentary_set.create(author=author, texto=comment_text, pub_data=timezone.now())
        return HttpResponseRedirect(reverse('fitness:resource_details', args=(resource.id,)))


def register_users(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user_type = request.POST['type-user']
        user = User.objects.create_user(username, email, password)

        utilizador = Utilizador(user=user, user_type=user_type)
        utilizador.save()

        if user_type == 'cliente':
            cliente = Cliente(utilizador=utilizador)
            cliente.save()
        else:
            funcionario = Funcionario(utilizador=utilizador)
            funcionario.save()

        return HttpResponseRedirect(reverse('fitness:login_users'))
    # GET request ou renderização inicial
    else:
        user_types = TypesOfUtilizador.choices()
        funcionario_cargos = Cargos.choices()
        print(user_types)
        context = {'user_types': user_types, 'funcionario_cargos': funcionario_cargos}
        return render(request, 'fitness/pagina_register.html', context)


def login_users(request):
    if request.method == 'POST' and request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if not request.user.is_superuser:  # Guardar id de aluno na session
                cliente_or_funcionario = get_object_or_404(Utilizador, user_id=user.id)

                if cliente_or_funcionario.user_type == 'cliente':
                    cliente = get_object_or_404(Cliente, utilizador_id=cliente_or_funcionario.id)
                    request.session['cliente_id'] = cliente.id
                else:
                    funcionario = get_object_or_404(Funcionario, utilizador_id=cliente_or_funcionario.id)
                    request.session['funcionario_id'] = funcionario.id

            return HttpResponseRedirect(reverse('fitness:index'))
        else:
            error_message = ("Username ou password inválida. Porfavor tente outra vez ou "
                             "registe uma nova conta.")
            return render(request, 'fitness/pagina_login.html',
                          {'error_message': error_message, 'entered_username': username,
                           'entered_password': password})
    # GET request ou renderização inicial
    else:
        return render(request, 'fitness/pagina_login.html')


def logout_users(request):
    request.session.flush()
    logout(request)
    return HttpResponseRedirect(reverse('fitness:index'))


@login_required
def user_info(request):
    # Inicializar variáveis
    cliente = None
    funcionario = None

    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = cliente.utilizador
    else:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = funcionario.utilizador

    user = utilizador.user
    context = {'utilizador': utilizador, 'cliente': cliente,
               'funcionario': funcionario}

    if request.method == 'POST' and request.POST:
        if 'email' in request.POST:
            user.email = request.POST['email']
        if request.POST['password'] == 'change':
            return HttpResponseRedirect(reverse('fitness:change_password'))
        if 'first_name' in request.POST:
            user.first_name = request.POST['first_name']
        if 'last_name' in request.POST:
            user.last_name = request.POST['last_name']
        if 'profile_picture' in request.FILES and utilizador:
            profile_picture = request.FILES['profile_picture']
            utilizador.profile_picture = profile_picture
        if cliente:
            if 'progresso_fitness' in request.POST:
                cliente.progresso_fitness = request.POST['progresso_fitness']
            if 'meta' in request.POST:
                cliente.progresso_fitness = request.POST['meta']
            if 'horario_treino' in request.POST:
                cliente.progresso_fitness = request.POST['horario_treino']
            if 'desafio' in request.POST:
                cliente.progresso_fitness = request.POST['desafio']
        else:
            if 'cargo' in request.POST:
                funcionario.progresso_fitness = request.POST['cargo']
            if 'horario_trabalho' in request.POST:
                funcionario.progresso_fitness = request.POST['horario_trabalho']

        user.save()
        utilizador.save()
        cliente.save() if cliente else funcionario.save()

        return HttpResponseRedirect(reverse('fitness:user_info'))
    # GET request ou renderização inicial
    else:
        return render(request, 'fitness/pagina_conta.html', context)


@login_required
def change_password(request):
    if request.session.get('cliente_id') is not None:
        cliente_id = request.session.get('cliente_id')
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        utilizador = cliente.utilizador
    else:
        funcionario_id = request.session.get('funcionario_id')
        funcionario = get_object_or_404(Funcionario, pk=funcionario_id)
        utilizador = funcionario.utilizador

    user = utilizador.user
    context = {'utilizador': utilizador}

    if request.method == 'POST' and request.POST:
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not check_password(old_password, user.password):
            error_message = "A password atual está incorreta."
        elif new_password1 != new_password2:
            error_message = "As novas passwords não coincidem. Confirme corretamente"
        else:
            user.set_password(new_password1)
            user.save()
            return HttpResponseRedirect(reverse('fitness:user_info'))

        # Caso houve algum erro
        context['error_message'] = error_message

    # Fazer render da página independentemente da situação
    return render(request, 'fitness/mudar_password.html', context)
