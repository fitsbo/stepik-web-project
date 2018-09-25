from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login, logout
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from qa.forms import AnswerForm, AskForm, AddUserForm, LoginUserForm
from qa.models import Answer, Question

# shortcut function to secure paginator, not implemented in code


def paginate(request, qs):
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page


@require_GET
def home(request):
    questions = Question.objects.new()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page='
    page = paginator.page(page)
    return render(request, 'home.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page, }
    )


@require_GET
def popular(request):
    questions = Question.objects.popular()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/popular/?page='
    page = paginator.page(page)
    return render(request, 'popular.html', {
        'questions': page.object_list,
        'paginator': paginator,
        'page': page, }
    )


def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        form._user = request.user
        if form.is_valid():
            question = form.save()
            url = question.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
        return render(request, 'ask.html', {
            'form': form,
        }
        )


def question(request, pk):
    def render_with_answers():
        try:
            answers = Answer.objects.filter(question_id=pk)
        except Answer.DoesNotExist:
            answers = None
        return render(request, 'question.html', {
            'question': question_page,
            'answers': answers,
            'form': form,
        })
    question_page = get_object_or_404(Question, id=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form._user = request.user
            form.save()
            url = question_page.get_absolute_url()
            return HttpResponseRedirect(url)
        else:
            form.cleaned_data['question'] = pk
            return render_with_answers()
    else:
        form = AnswerForm(initial={'question': pk})
        return render_with_answers()


def signup(request):
    if request.method == 'POST':
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            url = request.POST.get('continue', '/')
            return HttpResponseRedirect(url)
    else:
        form = AddUserForm()
    return render(request, 'signup.html',
                  {'form': form, }
                  )


def login_view(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            url = request.POST.get('continue', '/')
            return HttpResponseRedirect(url)
    else:
        form = LoginUserForm()
    return render(request, 'login.html',
                  {'form': form, }
                  )


def logout_view(request):
    logout(request)
    url = request.POST.get('continue', '/')
    return HttpResponseRedirect(url)


def test(request, *args, **kwargs):
    return HttpResponse('Ok')
