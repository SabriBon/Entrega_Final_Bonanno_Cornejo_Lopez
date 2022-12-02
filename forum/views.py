from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from forum.forms import ForumForm
from forum.models import Forum


class ForumListView(ListView):
    model = Forum
    paginate_by = 3


class ForumDetailView(DetailView):
    model = Forum
    template_name = "Forum/forum_detail.html"
    fields = ["name", "email","contact", "description"]

    def get(self, request, pk):
        forum = Forum.objects.get(id=pk)
        #comments = Comment.objects.filter(forum=forum).order_by("-updated_at")
        #comment_form = CommentForm()
        context = {
            "forum": forum,
        #    "comments": comments,
        #    "comment_form": comment_form,
        }
        return render(request, self.template_name, context)   


class ForumCreateView(LoginRequiredMixin, CreateView):
    model = Forum
    success_url = reverse_lazy("forum:forum-list")

    form_class = ForumForm


    def form_valid(self, form):
        """Filter to avoid duplicate accommodation"""
        data = form.cleaned_data
        form.instance.owner = self.request.user
        actual_objects = Forum.objects.filter(
            name=data["name"],
            email=data["email"],
            description=data["description"],
        ).count()
        if actual_objects:
            messages.error(
                self.request,
                f"El mensaje ya está registrado",
            )
            form.add_error("name", ValidationError("Acción no válida"))
            return super().form_invalid(form)
        else:
            messages.success(
                self.request,
                f"Mensaje registado exitosamente!",
            )
            return super().form_valid(form)


class ForumUpdateView(LoginRequiredMixin, UpdateView):
    model = Forum
    fields = ["name", "email", "contact", "description"]

    def get_success_url(self):
        forum = self.kwargs["pk"]
        return reverse_lazy("forum:forum-detail", kwargs={"pk": forum})


class ForumDeleteView(LoginRequiredMixin, DeleteView):
    model = Forum
    success_url = reverse_lazy("forum:forum-list")