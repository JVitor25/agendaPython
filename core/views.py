from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento

# Create your views here.

def data_eventos(request,titulo):
    object = Evento.objects.get(titulo)
    print("Object" + object)
    return HttpResponse('<h1>Data do evento: {}.</h1>'.format(object.data_evento))

def lista_eventos(request):
    usuario = request.user
    # evento = Evento.objects.filter(usuario=usuario) #Filtro por usuário
    evento = Evento.objects.all()
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

# def index(request):
#     return redirect('/agenda/')