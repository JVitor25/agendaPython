from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.models import Evento
from django.contrib import messages
# Create your views here.

def data_eventos(request,titulo):
    object = Evento.objects.get(titulo)
    print("Object" + object)
    return HttpResponse('<h1>Data do evento: {}.</h1>'.format(object.data_evento))

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario) #Filtro por usuário.
    # evento = Evento.objects.all() #Mostrar todos eventos para todos usuários.
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

# def index(request):
#     return redirect('/agenda/')

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválido!")
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')
