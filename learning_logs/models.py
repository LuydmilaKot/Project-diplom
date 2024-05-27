from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    '''Тема, которую изучает пользователь'''
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Возвращает строковое представление модели'''
        return self.text
    
class Entry(models.Model):
    '''Информация, изученная пользователем по теме'''
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # удаление статей по ключу "тема" в случае удаления темы -> каскадом
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True) # отображение записей по дате добавления и указания даты и времени

    class Meta: #использование множественной формы класса Entry при обращении более чем к одной записи
        verbose_name_plural = 'entries'

    def __str__(self):
        '''Возвращает строковое представление модели'''
        return f'{self.text[:50]}...' # отображает текст в пределах первых 50 символов
