from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
#no hace falta una view de logout en django 2.1 en adelante, sino q lo configuro en
#settings.py:

# My settings
#LOGOUT_REDIRECT_URL = '/'
#con eso le decimos a q pagina redireccionar cuando se haga el log out.

def register(request):
    """Registra un nuevo usuario."""
    if request.method != 'POST':
        #si no es POST, es GET, x lo q t da un formulario para registrarte
        form = UserCreationForm()
    else:
        #Procesa la data
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Al loguear seteo q redirija al home page
            authenticated_user = authenticate(username=new_user.username,
                                               password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))

    context = {'form' : form}
    return render(request, 'users/register.html', context)