# Migration: 0001_initial creado por Django.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration): # Clase que se encarga de crear las tablas en la base de datos.
    initial = True
    dependencies = [
    ]
    operations = [
        migrations.CreateModel(
            name='Password',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valid_pwd', models.TextField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('userID', models.IntegerField()),
                ('font_type', models.TextField(choices=[('Arial', 'Arial'), ('Verdana', 'Verdana'), ('Tahoma', 'Tahoma'), ('Trebuchet MS', 'Trebuchet MS'), ('Times New Roman', 'Times New Roman'), ('Georgia', 'Georgia'), ('Garamond', 'Garamond'), ('Helvetica', 'Helvetica'), ('Gill Sans', 'Gill Sans')], default='Verdana', null=True)),
                ('font_size', models.TextField(choices=[('Small', 'small'), ('Medium', 'medium'), ('Large', 'large')], default='Medium', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room_Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.user')),
            ],
        ),
        migrations.CreateModel(
            name='Room_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.user')),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.user'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('isimg', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.user')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decharlas.room')),
            ],
        ),
    ]
