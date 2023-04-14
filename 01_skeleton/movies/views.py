from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Movie, Comment
from .forms import MovieForm, CommentForm


def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


def create(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movies:detail', movie.pk)
    else:
        form = MovieForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/create.html', context)


def detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = movie.comment_set.all()
    context = {
        'movie': movie,
        'comments':comments,
        'comment_form':comment_form,
    }
    return render(request, 'movies/detail.html', context)


def delete(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user:
        movie.delete()
        return redirect('movies:index')
    return redirect('movies:detail', movie.pk)

def update(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.user == movie.user:
        if request.method == 'POST':
            form = MovieForm(request.POST, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('movies:detail', movie.pk)
        else:
            form = MovieForm(instance=movie)
    else:
        form = MovieForm(instance=movie)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/update.html', context)


#####


def comments_create(request, pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    movie = Movie.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
    return redirect('articles:detail', movie.pk)


def comments_delete(request, movie_pk, comment_pk):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    comment = Comment.objects.get(movie_pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('articles:detail', movie_pk)


@require_POST
def likes(request, article_pk):
    if request.user.is_authenticated:
        movie = Movie.objects.get(pk=article_pk)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:index')
    return redirect('accounts:login')
