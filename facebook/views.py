from django.shortcuts import render, redirect
from facebook.models import Article, Comment

# Create your views here.

def fail(request):
    return render(request, 'fail.html')

def help(request):
    return render(request, 'help.html')

def warn(request):
    return render(request, 'warn.html')

def newsfeed(request):
    articles = Article.objects.all()
    print(articles)
    return render(request, 'newsfeed.html', {'articles': articles})

def detail_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        Comment.objects.create(
            article=article,
            author=request.POST['author'],
            password=request.POST.get('password'),
            text=request.POST['text']
        )
        return redirect(f'/feed/{article.pk}')

    return render(request, 'detail_feed.html', {'feed': article})


def new_feed(request):
    if request.method == 'POST':
        new_article = Article.objects.create(
            author=request.POST['author'],
            title=request.POST['title'],
            password=request.POST['password'],
            text=request.POST['content'],
        )

        return redirect('/')

    return render(request, 'new_feed.html')

def edit_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        article.author = request.POST['author']
        article.title = request.POST['title']
        article.text = request.POST['content']

        if request.POST['password'] == article.password:
            article.save()
            return redirect(f'/feed/{article.pk}')

    return render(request, 'edit_feed.html', {'feed': article})

def remove_feed(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST':
        if request.POST['password'] == article.password:
            article.delete()
            return redirect('/')

    return render(request, 'remove_feed.html', {'feed': article})
