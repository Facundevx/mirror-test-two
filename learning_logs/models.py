from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Topic(models.Model):
    """Un topico que el usuario esta aprendiendo"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Devuelve un string del model"""
        return  self.text


class Entry(models.Model):
    """Cosas especificas de los topicos"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    #foreign key es un campo asociado a otro en una db.
    #esto es lo q conecta cada entry a un topic especifico
    #basicamente le da un valor a cada topic para asociarlo a cada pieza de info.
    #en text no ponemos un limite a textfield xq no queremos limitar la cantidad de caractes
    #por entry! y el datetimefield es para poner un timestamp de c/entry.

    class Meta:
        verbose_name_plural = 'entries'

    #aca se hace un nest de Meta, y lo q hace es cambiar en entry singular a plural si
    #hay mas de una!
    #la classe meta define la metadata de donde la ingreso

    def __str__(self):
        """devuelve un string representando al model"""
        return self.text[:50] + "..."

    #y en este campo le decimos q muestre hasta 50 caracteres x entry, tipo preview