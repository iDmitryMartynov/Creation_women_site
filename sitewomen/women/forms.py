from typing import Any
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.utils.deconstruct import deconstructible
from django.core.exceptions import ValidationError
from .models import Category, Husband


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None) -> None:
        self.message = message if message else 'Должны присутствовать только русские символы дефис и пробел'

    def __call__(self, value, *args: Any, **kwds: Any) -> Any:
        if not(set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label='Заголовок',
                            # validators=[
                            #     RussianValidator()
                            # ],
                            widget=forms.TextInput(attrs={'class': 'form-input'}), error_messages={
                            'min_length': 'Слишком короткий заголовок',
                            'required': 'Без заголовка никак'
                            })
    slug = forms.SlugField(max_length=255, label='URL',
                            validators=[
                                MinLengthValidator(5, message='Минимум 5 символов'),
                                MaxLengthValidator(100, message='Максимум 100 символов')
                            ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), required=False, label='Контент')
    is_published = forms.BooleanField(required=False, label='Статус', initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категории', empty_label='Категория не выбрана')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, label='Муж', empty_label="Не замужем")
    
    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
        if not(set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать только русские символы дефис и пробел')
    
