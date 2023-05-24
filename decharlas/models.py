#Descripción: Archivo que contiene los modelos de la base de datos

from django.db import models

class User(models.Model): #Usuario, tamaño y tipo de fuente.
    SIZE = [
        ("Small", "small"),
        ("Medium", "medium"),
        ("Large", "large"),
    ]
    FONT = [              
        ("Arial", "Arial"),
        ("Times New Roman", "Times New Roman"),
        ("Verdana", "Verdana"),
        ("Georgia", "Georgia"),
        ("Garamond", "Garamond"),
        ("Helvetica", "Helvetica"),
        ("Impact", "Impact"),
        ("Comic Sans MS", "Comic Sans MS"),
    ]
    name = models.TextField(max_length=100)
    userID = models.IntegerField()
    font_size = models.TextField(choices=SIZE, default="Medium", null=True)
    font_type = models.TextField(choices=FONT, default="Verdana", null=True)
    def __str__(self):
        return self.name + " -> " + str(self.userID)


class Room_Register(models.Model): #Registro de usuarios en una sala
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.name + " -> " + self.room.name


class Room(models.Model): #Sala de chat
    name = models.TextField(max_length=100)
    creator = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        return self.name + " -> " + self.creator.name


class Message(models.Model): #Mensaje
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    content = models.TextField()
    isimg = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.author.name + " ->" + self.content


class Password(models.Model): #Contraseña
    valid_pwd = models.TextField(max_length=10)
    def __str__(self):
        return "Password -> " + self.valid_pwd


class Room_Vote(models.Model): #Voto de una sala
    vote = models.BooleanField()
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    def __str__(self):
        if self.vote:
            value = "like"
        else:
            value = "dislike"
        return self.room.name + " | " + self.user.name + "->" + value







