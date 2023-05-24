#Descripcion: Archivo de pruebas unitarias para la aplicacion decharlas

from django.test import TestCase
from django.test import Client
from http.cookies import SimpleCookie
from .models import Password, User, Message, Room, Room_Register, Room_Vote

class GetTests (TestCase):
    def test_nocookie(self):  # Prueba que no se pueda acceder a la pagina sin cookie
        c = Client()
        response = c.get('/decharlas/')
        self.assertEqual(response.status_code, 302)

    def test_login(self): # Prueba que se pueda acceder a la pagina de login
        c = Client()
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)

    def test_root(self): # Prueba que se pueda acceder a la pagina principal
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.get('/decharlas/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<title>DeCharlas</title>', content)

    def test_room(self):  # Prueba que se pueda acceder a la pagina de una sala
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.post('/decharlas/', {'roomname': 'test_room'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/decharlas/test_room')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<label for="content">Enter Message</label>', content)

    def test_dynroom(self):  # Prueba que se pueda acceder a la pagina dinamica de una sala
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.post('/decharlas/', {'roomname': 'test_room'})
        self.assertEqual(response.status_code, 302)
        response = c.get('/decharlas/dyn/test_room')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>DYNAMIC ROOM</p>', content)

    def test_help(self): # Prueba que se pueda acceder a la pagina de ayuda
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.get('/decharlas/help')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        # self.assertIn('<label for="config_name">Name</label>', content)

    def test_config(self):  # Prueba que se pueda acceder a la pagina de configuracion
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.get('/decharlas/config')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<label for="config_name">Name</label>', content)

    def test_logout(self): # Prueba que se pueda acceder a la pagina de logout
        c = Client()
        Password.objects.create(valid_pwd='pass_1')
        response = c.get('/decharlas/login')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('<p>LOGIN DECHARLAS</p>', content)
        response = c.post('/decharlas/login', {'login_pwd': 'pass_1'})
        self.assertEqual(response.status_code, 302)
        self.client.cookies = SimpleCookie({'userID': User.objects.filter(id=1)})
        response = c.get('/decharlas/logout')
        self.assertEqual(response.status_code, 302)
