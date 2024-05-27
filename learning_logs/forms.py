from django import forms

from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    
    class Meta: # класс сообщает Django, на какой модели должна базироваться форма и какие поля на ней должны находиться
        model = Topic # форма создается на базе модели Topic
        fields = ['text'] # а на ней размещается только text
        labels = {'text': ''} # код приказывает Django не генерировать подпись для текстового поля
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': 'Entry:'} #снова назначается пустая запись
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} #элемент form.Textarea дает возможность сделать возможность ввода 80 столбцов
                                                               #вместо 40 по умолчанию
    