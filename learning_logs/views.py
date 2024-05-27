from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    '''Домашняя страница приложения Learning Log'''
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    '''Выводит список тем.'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    ''''''
    topic = Topic.objects.get(id=topic_id)
    # Проверка того, что тема принадлежит текущему пользователю.
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added') #сортировка дат в обратном порядке через минус
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    '''Определяет новую тему'''
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = TopicForm()
    else:
        # Отправлены данные POST; обработать данные
        form = TopicForm(data=request.POST)
        if form.is_valid(): # проверяет, что все обязательные поля заполнены
            form.save() # метод, который записывает данные из формы в базу данных
            return redirect('learning_logs:topics') # перенаправление пользователя к странице topics после отправки введенной темы (redirect)
    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    '''Добавляем новую запись по конкретной теме.'''
    topic = Topic.objects.get(id=topic_id) #идентификатор темы нужен для отображения страницы и обработки данных формы
    if request.method != 'POST':
        # Данные не отправлялись; создается пустая форма
        form = EntryForm()
    else:
        # Отправлены данные POST; обработать данные
        form = EntryForm(data=request.POST)
        if form.is_valid(): # проверяет, что все обязательные поля заполнены
            new_entry = form.save(commit=False) # создать объект без сохранения в БД
            new_entry.topic = topic #присваивание темы объекту
            new_entry.save() #сохранение в БД
            return redirect('learning_logs:topic', topic_id=topic_id) # перенаправление пользователя к странице темы, для кот. была создана запись
   
    # Вывести пустую или недействительную форму
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    '''Редактирует существующую запись.'''
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        # Исходный запрос; форма заполняется данными текущей записи
        form = EntryForm(instance=entry) #аргумент в скобках приказывает Django создать форму, заранее заполненную информацией из сущ. объекта записи
    else:
        # Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
        
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
        