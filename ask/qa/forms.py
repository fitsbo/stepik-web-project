from django import forms
from qa.models import Question, Answer


class AskForm(forms.Form):
    title = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']

    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question


class AnswerForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    question = forms.IntegerField()

    def clean_message(self):
        text = self.cleaned_data['text']

    def save(self):
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
