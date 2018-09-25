from django import forms
from django.contrib.auth.models import User
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data['title']
        return title

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        question = Question(**self.cleaned_data)
        question.author_id = self._user.id
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField(widget=forms.HiddenInput)

    def clean_question(self):
        question_id = self.cleaned_data['question']
        try:
            question = Question.objects.get(id=question_id)
        except question.DoesNotExist:
            question = None
        return question

    def clean_text(self):
        text = self.cleaned_data['text']
        return text

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.author_id = self._user.id
        answer.save()
        return answer


class AddUserForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea, max_length=100)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def save(self):
        user = User.objects.create_user(self.cleaned_data['username'],
                                        self.cleaned_data['email'],
                                        self.cleaned_data['password'])
        user.save()


class LoginUserForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
