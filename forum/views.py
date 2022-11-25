from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from forum.forms import ForumForm
from forum.models import Forum


def get_forum(request):
   forum = Forum.objects.all()
   paginator = Paginator(forum, 3)
   page_number = request.GET.get("page")
   return paginator.get_page(page_number)

def forum(request):
    return render(
        request=request,
        context={"forum_list": get_forum(request)},
        template_name="forum/forum_list.html",
    )   
def create_forum(request):
   if request.method == "POST":
       forum_form = ForumForm(request.POST)
       if forum_form.is_valid():
           data = forum_form.cleaned_data
           actual_objects = Forum.objects.filter(
               name=data["name"], email=data["email"]
           ).count()
           print("actual_objects", actual_objects)
           if not actual_objects:
                forum = Forum( 
                    name=data["name"],
                    email=data["email"], )
                forum.save()
                messages.success(
                    request,
                    f"Su reseña {data['name']} se agregó exitosamente!",
                )
                return render(
                    request=request,
                    context={"forum_list": get_forum(request)},
                    template_name="forum/forum_list.html",
                )

           else:
            messages.error(
                    request,
                    f"Su reseña {data['name']} ya está registrada",
                )


   forum_form = ForumForm(request.POST) 
   context_dict = {"form": forum_form}
   return render(
       request=request,
       context=context_dict,
       template_name="forum/forum_form.html",
   ) 
      
def forum_detail(request, pk: int):
    return render(
        request=request,
        context={"forum": Forum.objects.get(pk=pk)},
        template_name="forum/forum_detail.html",
    )


def forum_update(request, pk: int):
    forum = Forum.objects.get(pk=pk)

    if request.method == "POST":
        forum_form = ForumForm(request.POST)
        if forum_form.is_valid():
            data = forum_form.cleaned_data
            forum.name = data["name"]
            forum.email = data["email"]
            forum.contact = data["contact"]
            forum.description = data["description"]
            forum.save()

            return render(
                request=request,
                context={"forum": forum},
                template_name="forum/forum_detail.html",
            )

    forum_form = ForumForm(model_to_dict(forum))
    context_dict = {
        "forum": forum,
        "form": forum_form,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="forum/forum_form.html",
    )


def forum_delete(request, pk: int):
    forum = Forum.objects.get(pk=pk)
    if request.method == "POST":
        forum.delete()

        forum = Forum.objects.all()
        context_dict = {"forum_list": forum}
        return render(
            request=request,
            context=context_dict,
            template_name="forum/forum_list.html",
        )

    context_dict = {
        "forum": forum,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="forum/forum_confirm_delete.html",
    )


class ForumListView(ListView):
    model = Forum
    paginate_by = 3


class ForumDetailView(DetailView):
    model = Forum
    fields = ["name", "email","contact", "description"]


class ForumCreateView(CreateView):
    model = Forum
    success_url = reverse_lazy("forum:forum-list")

    form_class = ForumForm
    fields = ["name", "email", "description"]

    def form_valid(self, form):
        """Filter to avoid duplicate accommodations"""
        data = form.cleaned_data
        actual_objects = Forum.objects.filter(
            description=data["description"],
        ).count()
        if actual_objects:
            messages.error(
                self.request,
                f"El meensaje {data['description']} ya fue registrado anteriormente",
            )
            form.add_error("name", ValidationError("Acción no válida"))
            return super().form_invalid(form)
        else:
            messages.success(
                self.request,
                f"Mensaje {data['description']} subido exitosamente!",
            )
            return super().form_valid(form)


class ForumUpdateView(UpdateView):
    model = Forum
    fields = ["name", "email", "description"]

    def get_success_url(self):
        forum_id = self.kwargs["pk"]
        return reverse_lazy("forum:forum-detail", kwargs={"pk": forum_id})


class ForumDeleteView(DeleteView):
    model = Forum
    success_url = reverse_lazy("forum:forum-list")
    
