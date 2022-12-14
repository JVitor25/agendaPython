from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from core.models import Evento
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.


def data_eventos(request,titulo):
    object = Evento.objects.get(titulo)
    print("Object" + object)
    return HttpResponse('<h1>Data do evento: {}.</h1>'.format(object.data_evento))



@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,#Filtro por usuário.
                                   data_evento__gt=data_atual) #Filtro por data
    # evento = Evento.objects.all() #Mostrar todos eventos para todos usuários.
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)


@login_required(login_url='/login/')
def json_lista_evento(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo')
    return JsonResponse(list(evento), safe=False)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get("id_evento")
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                Evento.objects.filter(id=id_evento).update(titulo=titulo,
                                                           data_evento=data_evento, 
                                                           descricao=descricao)
            # Outra forma de fazer:
            # evento.titulo = titulo
            # evento.descricao = descricao
            # evento.data_evento = data_evento
            # evento.save()
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento, 
                                  descricao=descricao, 
                                  usuario=usuario)
    return redirect('/')



@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)



# def index(request):
#     return redirect('/agenda/')



def login_user(request):
    return render(request, 'login.html')



@login_required(login_url='/login/')
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


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    
    try: 
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()
    
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')

def logout_user(request):
    logout(request)
    return redirect('/')
