#Descripcion: Archivo que contiene las funciones que manejan las vistas de la aplicacion

from django.http import HttpResponse, JsonResponse, Http404
from .models import Message, Room, User, Password, Room_Register, Room_Vote
from .forms import Font_Formulario
from django.template import loader
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import random
import json

class Stats:
    def __init__(self):
        self.text = Message.objects.filter(isimg=False).count()  # Numero de mensajes de texto
        self.img = Message.objects.filter(isimg=True).count()    # Numero de mensajes de imagen
        self.users = User.objects.all().count()           # Numero de usuarios

# Funcion que maneja el login de la aplicacion
def login(request):
    if request.method == 'GET' or request.method == 'POST':
        if request.method == 'POST':
            input_pwd = request.POST['login_pwd']
            try:
                Password.objects.get(valid_pwd=input_pwd)
                userID = random.randint(1000, 9999)   # Generar un userID aleatorio
                name = "Anonymous_" + str(userID)    # Generar un nombre de usuario con el ID
                new_user = User(name=name, userID=userID)
                new_user.save()
                final_res = redirect('/decharlas/')
                final_res.set_cookie("userID", userID)  # Establecer la cookie con el userID
                return final_res
            except Password.DoesNotExist:
                context = {
                    'failed_post': True,
                }
        if request.method == 'GET':
            context = {
                'failed_post': False,
            }
        template = loader.get_template('decharlas/login.html')
        return HttpResponse(template.render(context, request))
    else:
         return HttpResponse('Page not exist')


def nuevaSala(request, user_info):     # Funcion que crea una nueva sala
    room_name = request.POST["roomname"]
    if room_name == "":
        return redirect('/decharlas/')
    try:
        room = Room.objects.get(name=room_name)
    except Room.DoesNotExist:
        new_room = Room(name=room_name, creator=user_info)
        new_room.save()
        room = Room.objects.get(name=room_name)
    final_res = redirect('/decharlas/' + room.name)
    return final_res


def salaNoLeida(user_info):     # Funcion que devuelve el numero de salas no leidas
    room_list = Room.objects.all()
    unread_list = []
    for room in room_list:
        try:
            user_register = Room_Register.objects.get(user=user_info, room=room)
            msg_count = 0
            msg_list = Message.objects.filter(room=room)
            if not msg_list:
                unread_list.append('-1')
            else:
                for message in msg_list:
                    if message.date >= user_register.date and message.author != user_info:
                        msg_count += 1
                unread_list.append(msg_count)
        except Room_Register.DoesNotExist:
            unread_list.append('-1')
    return unread_list


def mensajesTotal():          # Funcion que devuelve el numero total de mensajes
    room_list = Room.objects.all()
    total_list =[]
    for room in room_list:
        room_total = Message.objects.filter(room=room).count()
        total_list.append(room_total)
    return total_list


# Funcion que maneja el logout de la aplicacion
def logout(request):
    final_res = redirect('/decharlas/login')
    final_res.delete_cookie('userID')
    return final_res


def vote_list():         # Funcion que devuelve la lista de votos
    room_list = Room.objects.all()
    vote_list = []
    for room in room_list:
        like_votes = Room_Vote.objects.filter(room=room, vote=True).count()
        dislike_vote = Room_Vote.objects.filter(room=room, vote=False).count()
        room_votes = {
            "likes": str(like_votes),
            "dislikes": str(dislike_vote),
        }
        vote_list.append(room_votes)
    return vote_list


def update_vote(request, user_info, room_info):        # Funcion que actualiza los votos
    action = request.POST.get('action')
    action_vote = action == 'like'
    try:
        user_vote = Room_Vote.objects.get(room=room_info, user=user_info)
        if user_vote.vote != action_vote:
            user_vote.vote = action_vote
            user_vote.save()
    except Room_Vote.DoesNotExist:
        user_vote = Room_Vote(room=room_info, user=user_info, vote=action_vote)
        user_vote.save()


def general(request):      # Funcion que maneja la pagina principal
    if request.method == 'GET' or request.method == 'POST':
        if 'userID' in request.COOKIES:    # Comprobar si el usuario esta logueado
            user_ID = request.COOKIES['userID']
        else:
            return redirect('/decharlas/login')
        user_info = User.objects.get(userID=user_ID)
        if request.method =="GET":
            template = loader.get_template('decharlas/general.html')
            room_list = Room.objects.all()
            main_stats = Stats()
            context = {
                'user_info': user_info,   # Informacion del usuario
                'room_list': room_list,   # Lista de salas
                'salaNoLeida': salaNoLeida(user_info),   # Lista de salas no leidas
                'vote_list': vote_list(),    # Lista de votos
                'total_msg': mensajesTotal(),   # Lista de mensajes totales
                'stats': main_stats,   # Estadisticas
            }
            final_res = HttpResponse(template.render(context, request))    # Respuesta final
        else:
            final_res = nuevaSala(request, user_info)     # Crear una nueva sala
        return final_res
    else:
        raise Http404      # Error 404

def help(request):    # Funcion que maneja la pagina de ayuda
    if request.method == 'GET' or request.method == 'POST':
        if 'userID' in request.COOKIES:   # Comprobar si el usuario esta logueado
            user_ID = request.COOKIES['userID']
        else:
            return redirect('/decharlas/login')
        user_info = User.objects.get(userID=user_ID)
        if request.method == "GET":
            template = loader.get_template('decharlas/help.html')
            main_stats = Stats()
            context = {
                'user_info': user_info,    # Informacion del usuario
                'stats': main_stats,     # Estadisticas
            }
            final_res = HttpResponse(template.render(context, request))    # Respuesta final
        else:
            return nuevaSala(request, user_info)   # Crear una nueva sala
        return final_res
    else:
        raise Http404


def config(request):    # Funcion que maneja la pagina de configuracion
    if request.method == 'GET' or request.method == 'POST':
        if 'userID' in request.COOKIES:
            user_ID = request.COOKIES['userID']
        else:
            return redirect('/decharlas/login')
        user_info = User.objects.get(userID=user_ID)
        if request.method == "GET":
            template = loader.get_template('decharlas/config.html')
            form = Font_Formulario
            main_stats = Stats()
            context = {
                'user_info': user_info,
                'form': form,
                'stats': main_stats,
            }
            final_res = HttpResponse(template.render(context, request))
        else:
            action = request.POST.get('action')
            if action == "nuevaSala":
                return nuevaSala(request, user_info)
            font_type = request.POST['font_type']   # Actualizar la configuracion del usuario
            font_size = request.POST['font_size']
            new_name = request.POST['config_name']
            if not new_name == "":
                user_info.name = new_name
            user_info.font_type = font_type
            user_info.font_size = font_size
            user_info.save()
            final_res = redirect('/decharlas/')
        return final_res
    else:
        raise Http404


def user_register(room, user):     # Funcion que maneja el registro de usuarios en salas
    try:
        user_register = Room_Register.objects.get(user=user, room=room)
        user_register.date = timezone.now()
        user_register.save()
    except Room_Register.DoesNotExist:
        user_register = Room_Register(user=user,
                                      room=room,
                                      date=timezone.now())
        user_register.save()


def rsc(request, resource):                # Funcion que maneja los recursos
    if resource == 'script.js':
        return HttpResponse('/decharlas/script.js')
    if request.method == "GET" or request.method == "POST":
        if 'userID' in request.COOKIES:
            user_ID = request.COOKIES['userID']
        else:
            return redirect('/decharlas/login')
        user_info = User.objects.get(userID=user_ID)
        room_info = Room.objects.get(name=resource)
        if request.method == "POST":
            action = request.POST.get('action')
            if action == "nuevaSala":
                return nuevaSala(request, user_info)
            elif action == 'like' or action == 'dislike':
                update_vote(request, user_info, room_info)
                return redirect('/decharlas/' + room_info.name)
            else:
                newmsg(request, room_info, user_info)
        user_register(room_info, user_info)
        msg_list = Message.objects.filter(room=room_info)
        template = loader.get_template('decharlas/room.html')
        main_stats = Stats()
        context = {
            'user_info': user_info,
            'msg_list': msg_list,
            'stats': main_stats,
        }
        final_res = HttpResponse(template.render(context, request))
        return final_res
    else:
        raise Http404


def newmsg(request, room, user):    # Funcion que maneja la creacion de mensajes
    msg_content = request.POST['content']
    msg_isimg = request.POST.get('isimg', False)
    if msg_isimg == 'on':
        msg_isimg = True   # Comprobar si el mensaje es una imagen
    else:
        msg_isimg = False
    msg_date = timezone.now()
    new_msg = Message(content=msg_content,
                      date=msg_date,
                      isimg=msg_isimg,
                      author=user,
                      room=room)
    new_msg.save()


def dynrsc(request, resource):      # Funcion que maneja los recursos dinamicos.
    if request.method == "GET" or request.method == "POST":
        if resource == 'script.js':
            return HttpResponse('script.js')
        print("Método ->" + request.method)
        if 'userID' in request.COOKIES:
            user_ID = request.COOKIES['userID']
        else:
            return redirect('/decharlas/login')
        print("Resource ->" + resource)
        user_info = User.objects.get(userID=user_ID)
        room_info = Room.objects.get(name=resource)
        if request.method == "POST":
            action = request.POST.get('action')
            if action == "nuevaSala":
                return nuevaSala(request, user_info)
            elif action == 'like' or action == 'dislike':
                update_vote(request, user_info, room_info)
                return redirect('/decharlas/' + room_info.name)
            else:
                newmsg(request, room_info, user_info)
        user_register(room_info, user_info)
        template = loader.get_template('decharlas/dynroom.html')
        main_stats = Stats()
        context = {
            'user_info': user_info,
            'room_info': room_info,
            'stats': main_stats,
        }
        final_res = HttpResponse(template.render(context, request))
        return final_res
    else:
        raise Http404


def jsonrsc(request, resource):     # Funcion que maneja los recursos JSON, implementar.
    if request.method == "GET" or request.method == "POST":
        print("Método ->" + request.method)
        if 'userID' in request.COOKIES:
            pass
        else:
            return redirect('/decharlas/login')
        room_info = Room.objects.get(name=resource)
        msg_list = Message.objects.filter(room=room_info)
        msg_dict_list = []
        for msg in msg_list:
            msg_dict = {
                "author": msg.author.name,
                "text": msg.content,
                "isimg": msg.isimg,
                "date": msg.date,
            }
            msg_dict_list.append(msg_dict)
        json_list = JsonResponse(msg_dict_list, safe=False)
        return json_list

    else:
        raise Http404