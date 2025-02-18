# Create your views here.
from django.shortcuts import render
from .models import Topic
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def index(request):
    """Página principal do Learning_Log."""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """Mostra todos os assuntos."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Mostra as informações sobre determinado assunto."""
    topic = Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """Adiciona um novo assunto."""
    if request.method != 'POST':
        # Nenhum dado enviado; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST enviados; processa os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


def new_entry(request, topic_id):
    """Acresenta uma nova entrada para um assunto escolhido."""
    topic = Topic.objects.get(id = topic_id)

    if request.method != 'POST':
        # Nenhum dado enviado; cria um formulário em branco
        form = EntryForm()
    else:
        # Dados de POST enviados; processa os dados
        form = EntryForm(data=request.POST) 
        if form.is_valid():
            new_entry = form.save(commit=False) # Cria um objeto mas não salva no BD.
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic', args=[topic_id]))
        
    context = {'topic':topic, 'form':form}
    return render(request, 'learning_logs/new_entry.html', context)
    
