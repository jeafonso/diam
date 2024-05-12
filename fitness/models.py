import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from enum import Enum
from django.templatetags.static import static


class TypesOfResource(Enum):
    WORKOUT = 'workout'
    NUTRITION = 'nutrition'
    HEALTH = 'health'
    MISCELLANEA = 'miscellanea'

    @classmethod
    def choices(cls):
        return [(types.value, types.name) for types in cls]


class TypesOfUtilizador(Enum):
    CLIENTE = 'cliente'  # Tipo de utilizador: Cliente
    FUNCIONARIO = 'funcionario'  # Tipo de utilizador: Funcionário

    @classmethod
    def choices(cls):
        return [(types.value, types.name) for types in cls]


class Cargos(Enum):
    INSTRUTOR = 'instrutor'  # Cargo: Instrutor
    RECECIONISTA = 'rececionista'  # Cargo: Rececionista
    GERENTE = 'gerente'  # Cargo: Gerente
    PT = 'pt'  # Cargo: Personal Trainer
    LIMPEZA = 'limpeza'  # Cargo: Limpeza
    NUTRICIONISTA = 'nutricionista'  # Cargo: Nutricionista

    @classmethod
    def choices(cls):
        return [(types.value, types.name) for types in cls]


class TypesOfDesafio(Enum):
    FITNESS = 'fitness'
    NUTRITION = 'nutrition'
    ENDURANCE = 'endurance'
    STRENGTH = 'strength'
    WEIGHT_LOSS = 'weight_loss'
    FLEXIBILITY = 'flexibility'
    CARDIO = 'cardio'
    MUSCLE_GAIN = 'muscle_gain'
    CORE_STABILITY = 'core_stability'
    HIIT = 'hiit'
    YOGA = 'yoga'
    CROSSFIT = 'crossfit'

    @classmethod
    def choices(cls):
        return [(types.value, types.name) for types in cls]


# Utilizador
class Utilizador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, default='default_pfp.jpg')
    user_type = models.CharField(max_length=20, choices=[(types.value, types.name) for types in TypesOfUtilizador])

    def __str__(self):
        # Retorna o nome do utilizador
        return self.user.username


# Desafios
class Desafio(models.Model):
    nome = models.CharField(max_length=200)
    type = models.CharField(max_length=50, choices=[(types.value, types.name) for types in TypesOfDesafio])
    descricao = models.CharField(max_length=200)
    data_inicio = models.DateField('data de inicio')
    data_fim = models.DateField('data de encerramento')
    regras = models.CharField(max_length=200)
    participantes = models.ManyToManyField(Utilizador, related_name='desafios')

    def __str__(self):
        # Retorna o nome do desafio
        return self.nome


# Cliente
class Cliente(models.Model):
    utilizador = models.OneToOneField(Utilizador, on_delete=models.CASCADE)
    meta = models.TextField(default="")
    horarios_treino = models.CharField(max_length=200, blank=True, null=True)
    progresso_fitness = models.TextField(blank=True, default="")

    def __str__(self):
        # Retorna o nome do cliente
        return self.utilizador.user.username


# Funcionário
class Funcionario(models.Model):
    utilizador = models.OneToOneField(Utilizador, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=20, choices=[(cargos.value, cargos.name) for cargos in Cargos])
    horario_trabalho = models.DateTimeField('horario de trabalho', blank=True, null=True)

    def __str__(self):
        # Retorna o nome do funcionário
        return self.utilizador.user.username


# Aulas/Treinos
class Aula(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.CharField(max_length=200)
    instrutor = models.ForeignKey(Funcionario, on_delete=models.CASCADE)
    horario = models.DateTimeField('horario de aula')
    max_participantes = models.IntegerField(default=0)
    participantes = models.ManyToManyField(Utilizador, related_name='aulas')

    def __str__(self):
        # Retorna o nome da aula
        return self.nome


# Posts do fórum
class Post(models.Model):
    autor = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, default="")
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        # Retorna o assunto do post
        return self.titulo


class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto = models.TextField(default="")
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.texto


class Resource(models.Model):
    author = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=[(types.value, types.name) for types in TypesOfResource])
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.title


class Commentary(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    author = models.ForeignKey(Utilizador, on_delete=models.CASCADE)
    texto = models.TextField(default="")
    pub_data = models.DateTimeField('data de publicacao')

    def __str__(self):
        return self.texto
