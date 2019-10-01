from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, ModelFormMixin
from .models import Post, Comment
from .forms import PostModelForm, CommentModelForm


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.id
    if comment.author == request.user:
        comment.delete()
    return redirect('post_detail', pk=post_pk)


class PostListView(ListView):
    model = Post
    paginate_by = 8
    

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(ModelFormMixin, DetailView):
    model = Post
    form_class = CommentModelForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['comment_list'] = Comment.objects.filter(post=self.object)
        context['is_user'] = get_user_model().objects.filter(id=self.request.user.id)
        return context

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.author = self.request.user
        comment.save()
        return redirect('post_detail', pk=self.get_object().id)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid() and get_object_or_404(get_user_model(), pk=request.user.id):
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostModelForm

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model       = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

