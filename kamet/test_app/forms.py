from django import forms
from .import models
from django.contrib.auth import get_user_model
 
class TopicForm(forms.ModelForm):
    class Meta:
        model = models.Topics
        fields = ['subject','time_allotted','number_questions']
        widgets = {
            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    'placeholder':"Enter topic subject name ..."
                }
            ),
            "time_allotted": forms.NumberInput(
                attrs={
                    "style": "max-width: 100px;",
                    "class": "form-control",

                }
            ),
            "number_questions": forms.NumberInput(
                attrs={
                    "style": "max-width: 100px;",
                    "class": "form-control",

                }
            ),
        }

class UserForm(forms.ModelForm):
    attempts = forms.CharField(label="Attempts", max_length=100, widget=forms.NumberInput(attrs={"class": "form-control", "style": "max-width: 100px;",'placeholder':"Enter number of attempts for user ..."}))
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email']
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter the username for user ..."
                }
            ),
            "password": forms.PasswordInput(
                attrs={
                    "style": "max-width: 500px;",
                    "class": "form-control",
                    'placeholder':"Enter the password for user ..."

                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "style": "max-width: 500px;",
                    "class": "form-control",
                    'placeholder':"Enter the email-id of user ..."

                }
            ),
        }
        
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = models.TestUser
        fields = ['attempts']
        widgets = {
            "attempts": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter the username for user ..."
                }
            ),
        }
        
class QuestionForm(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = ['question_text','option_a','option_b','option_c','option_d','option_correct']
        widgets = {
            "topics": forms.Select(
                attrs={
                    "style": "max-width: 700px;",
                    'rows': 5,
                    'placeholder':"Enter the Question..."
                }
            ),
            "question_text": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 700px;",
                    'rows': 5,
                    'placeholder':"Enter the Question..."
                }
            ),
            "option_a": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter option A..."
                }
            ),
            "option_b": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter option B..."
                }
            ),
            "option_c": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter option C..."
                }
            ),
            "option_d": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 500px;",
                    'placeholder':"Enter option D..."
                }
            ),
            "option_correct": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "max-width: 100px;",
                    'maxlength':1,
                    'placeholder':"Enter the correct option..."  
                }
            ),
        }
        labels = {
            'question_text': 'Question',
            'option_a': 'Option A',
            'option_b': 'Option B',
            'option_c': 'Option C',
            'option_d': 'Option D',
            'option_correct': 'Correct Option',
        }