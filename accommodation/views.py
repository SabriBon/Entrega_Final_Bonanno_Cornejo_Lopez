from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView



from accommodation.forms import CommentForm
from accommodation.forms import AccommodationForm
from accommodation.models import Accommodation
from accommodation.models import Comment



class AccommodationListView(ListView):
    model = Accommodation
    paginate_by = 3


class AccommodationDetailView(DetailView):
    model = Accommodation
    template_name = "accommodation/accommodation_detail.html"
    fields = ["name", "location","contact","price", "description"]

    def get(self, request, pk):
        accommodation = Accommodation.objects.get(id=pk)
        comments = Comment.objects.filter(accommodation=accommodation).order_by("-updated_at")
        comment_form = CommentForm()
        context = {
            "accommodation": accommodation,
            "comments": comments,
            "comment_form": comment_form,
        }
        return render(request, self.template_name, context)   


class AccommodationCreateView(LoginRequiredMixin, CreateView):
    model = Accommodation
    success_url = reverse_lazy("accommodation:accommodation-list")

    form_class = AccommodationForm
    #fields = ["name", "location","contact","price", "description"]

    def form_valid(self, form):
        """Filter to avoid duplicate accommodation"""
        data = form.cleaned_data
        form.instance.owner = self.request.user
        actual_objects = Accommodation.objects.filter(
            name=data["name"],
        ).count()
        if actual_objects:
            messages.error(
                self.request,
                f"El alojamiento {data['name']} ya está registrado",
            )
            form.add_error("name", ValidationError("Acción no válida"))
            return super().form_invalid(form)
        else:
            messages.success(
                self.request,
                f"Alojamiento {data['name']} agregado exitosamente!",
            )
            return super().form_valid(form)


class AccommodationUpdateView(LoginRequiredMixin, UpdateView):
    model = Accommodation
    fields = ["name","contact", "price", "description"]

    def get_success_url(self):
        accommodation_id = self.kwargs["pk"]
        return reverse_lazy("accommodation:accommodation-detail", kwargs={"pk": accommodation_id})


class AccommodationDeleteView(LoginRequiredMixin, DeleteView):
    model = Accommodation
    success_url = reverse_lazy("accommodation:accommodation-list")

class CommentCreateView(LoginRequiredMixin, CreateView):
    def post(self, request, pk):
        accommodation = get_object_or_404(Accommodation, id=pk)
        comment = Comment(
            text=request.POST["comment_text"], owner=request.user, accommodation=accommodation
        )
        comment.save()
        return redirect(reverse("accommodation:accommodation-detail", kwargs={"pk": pk}))


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        accommodation = self.object.accommodation
        return reverse("accommodation:accommodation-detail", kwargs={"pk": accommodation.id})






