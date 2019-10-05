from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail
from .models import Post, PostCategory, Comment
from .forms import PostModelForm, PostCommentForm, PostEmailForm, SearchForm
from taggit.models import Tag
from django.db.models import Count
from haystack.query import SearchQuerySet

# Create your views here.


def post_share(request, slug):
    post = get_object_or_404(Post, slug=slug, published=True)
    sent = False

    if request.method == 'POST':
        form = PostEmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you read "{}"'.format(
                cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title, post_url, cd['name'], cd['comment'])
            send_mail(subject, message, 'neupytechng@gmail.com', [cd['to']])
            sent = True
    else:
        form = PostEmailForm()
    context = {
        'form': form,
        'post': post,
        'sent': sent,
        'title': 'Post Share'
    }
    return render(request, 'post/share.html', context)


class PostListView(ListView):
    tag_slug = None
    tag = None
    category_slug = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    model = Post
    queryset = Post.objects.filter(published=True)
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 20


class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_post.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created_at')


def details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = PostCommentForm(data=request.POST)
        if comment_form.is_valid():
            new_commment = comment_form.save(commit=False)
            new_commment.post = post
            new_commment.save()

    else:
        comment_form = PostCommentForm
    posts_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(
        tags__in=posts_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count(
        'tags')).order_by('-same_tags', '-published')[:4]

    context = {
        'title': 'Blog Details',
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'similar_posts': similar_posts
    }
    return render(request, 'post/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post/post_create.html'
    form_class = PostModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = 'post/post_create.html'
    queryset = Post.objects.all()
    form_class = PostModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('post:blog-home')


def featured_view(request):
    featured_post = Post.objects.filter(featured=True)
    print(featured_post)
    context = {
        'featured_post': featured_post,
        'title': 'Featured Posts'
    }

    return render(request, 'post/home.html', context)


def search_view(request):
    search_form = SearchForm()
    if 'query' in request.GET:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            cd = search_form.cleaned_data
            results = SearchQuerySet().models(Post).filter(
                content=cd['query']).load_all()

            total_results = results.count()
        context = {
            'search_form': search_form,
            'total_results': total_results,
            'results': results,
            'cd': cd,
            'title': 'Search'
        }
        return render(request, 'post/search.html', context)
    return render(request, 'post/search.html', {'search_form': search_form})


class CategoryListView(ListView):
    model = Post
    template_name = 'post/category.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(
            PostCategory, slug=self.kwargs['slug'])
        return Post.objects.filter(category=self.category, published=True)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['category'] = self.category
        return data
    # model = Post
    # template_name = 'post/user_post.html'
    # context_object_name = 'posts'
    # paginate_by = 20

    # def get_queryset(self):
    #     category = get_object_or_404(Post, slug=self.kwargs.get('slug'))
    #     return Post.objects.filter(cat_title=category).order_by('-created_at')
