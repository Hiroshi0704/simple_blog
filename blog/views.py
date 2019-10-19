from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, ModelFormMixin
from django.db.models import Q
from .models import Post, Comment
from .forms import PostModelForm, CommentModelForm

User = get_user_model()

def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.id
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=post_pk)


class PostListView(ListView):
    model = Post
    paginate_by = 8

    def post(self, request, *args, **kwargs):
        request.session['search_value'] = request.POST.get('search', None)
        return self.get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_value = ''
        if 'search_value' in self.request.session:
            search_value = self.request.session['search_value']
        context['search_value'] = search_value
        return context

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset().select_related('author')

        if 'search_value' in self.request.session:
            keyword = self.request.session['search_value'].split(' ')
            for key in keyword:
                queryset = queryset.filter(Q(title__icontains=key) | Q(body__icontains=key) | Q(author__username__icontains=key))
        return queryset
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'"{form.instance.title}" has been created!')
        return super().form_valid(form)


class PostDetailView(ModelFormMixin, DetailView):
    model = Post
    form_class = CommentModelForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        comment_list = Comment.objects.filter(post=self.object)
        context['comment_list'] = comment_list
        context['is_user'] = User.objects.filter(id=self.request.user.id)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        return redirect('post_detail', pk=self.get_object().id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and get_object_or_404(User, pk=request.user.id):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostModelForm

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        messages.info(self.request, f'"{form.instance.title}" has been updated!')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model       = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        message = f'"{self.object.title}" has been deleted.'
        messages.warning(request, message)
        return result