from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.core.files.storage import FileSystemStorage


# A ser usado no decorator @user_passes_test, testar é um funcionário ou superuser
def admin_check(request, user):
    return (user.is_authenticated and user.is_superuser) or request.session.get('funcionario_id') is not None


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


def class_page(request):
    aulas = Aula.objects.all()
    return render(request, 'fitness/marcar_aulas.html', {"aulas": aulas})


def class_signup(request, aula_id):
    aula = Aula.objects.get(id=aula_id)
    if request.user.is_authenticated and request.method == 'POST':
        if aula.participantes.count() < aula.max_participantes:
            aula.participantes.add(request.user)
            return render(request, 'fitness/marcar_aulas.html')  # Redirect to class schedule page
        else:
            error_message = "Class is full!"
            return render(request, 'fitness/signup_error.html', {'error_message': error_message})
    else:
        return render(request, 'fitness/pagina_login.html')


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

    forum_post_list = Post.objects.order_by('-pub_data')[:10]

    context = {'forum_post_list': forum_post_list}
    if utilizador:
        context['utilizador'] = utilizador

    return render(request, 'fitness/forum.html', context)


def post_detalhes(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    utilizador = None

    #if request.method == 'POST' and request.POST:
    #    post.delete()
    #    return HttpResponseRedirect(reverse('fitness:index'))

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


@login_required
def voto(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)

    try:
        opcao_seleccionada = questao.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        # Apresenta de novo o form para votar
        return render(request, 'fitness/detalhe.html', {
            'questao': questao,
            'error_message': "Não escolheu uma opção!",
        })
    else:
        if 'Votar' in request.POST['submit_action']:
            if not request.user.is_superuser:
                aluno = get_object_or_404(Aluno, user_id=request.user.id)
                if aluno.votos < 7:
                    aluno.votos += 1
                    aluno.save()
                else:
                    return render(request, 'fitness/detalhe.html', {
                        'questao': questao,
                        'error_message': "Atingiu o seu limite de votos!",
                    })

            opcao_seleccionada.votos += 1
            opcao_seleccionada.save()
            return HttpResponseRedirect(
                reverse('fitness:resultados', args=(questao.id,)))

        elif 'Apagar opção' in request.POST['submit_action']:
            opcao_seleccionada.delete()
            return HttpResponseRedirect(
                reverse('fitness:detalhe', args=(questao.id,)))
    return None


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
def create_comentario(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST' and request.POST:
        texto_comentario = request.POST['comment_texto']
        autor = get_object_or_404(Utilizador, user=request.user)

        comentario = post.comentario_set.create(autor=autor, texto=texto_comentario, pub_data=timezone.now())
        return HttpResponseRedirect(reverse('fitness:post_detalhes', args=(post.id,)))


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
        print(user_types)
        context = {'user_types': user_types}
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
