from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

#Esta funcion hace un render de la respuesta en base a la data q le provee el views
#entonces seteo una view para la home page
#usa dos argumentos, un request y un template
#esta va a ser mi home page

def index(request):
    """Home page para learning log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Pagina de topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Muestra cada topic y toda su info"""
    topic = Topic.objects.get(id=topic_id)
    #verifica q el topic corresponda al usuario, por seguridad.
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """anade un nuevo topico"""
    if request.method != 'POST':
        # Si no se ingresa data, crea un formulario en blanco
        form = TopicForm
    else:
        #Si se ingresa data, se procesa
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Anade una entry a un topic particular"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm()
    else:
        #proceso la data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))
    #el commit false hace q se cree un nuevo entry object pero no lo guarda en la db todavia
    #hasta q le de .save
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
    #dsp con el return http hace q el usuario vuelva a la pagina de topic y necesita dos argumentos
    #un pattern de la url q queremos generar y un args de lista, q contiene cualquier argumento
    #nescerio para generar la url

@login_required
def edit_entry(request, entry_id):
    """Edita un entry existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #me devuelve la entry q estaba guardada
        form = EntryForm(instance=entry)
    else:
        #postea la data editada y la procesa
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

#un context es un diccionario en el q las keys son los nombres q usamos en el
#template para acceder a la data y los valores son la data q tenemos q mandar
#al template