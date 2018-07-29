from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm


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
    question_page = get_object_or_404(Question, id=pk)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            url = question_page.get_absolute_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm(initial={'question': pk})
        try:
            answers = Answer.objects.filter(question_id=pk)
        except Answer.DoesNotExist:
            answers = None
        return render(request, 'question.html', {
            'question': question_page,
            'answers': answers,
            'form': form,
        }
        )


def test(request, *args, **kwargs):
    return HttpResponse('Ok')
