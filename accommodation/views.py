from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


from accommodation.forms import CommentForm
from accommodation.forms import AccommodationForm
from accommodation.models import Accommodation
from accommodation.models import Comment


#def get_accommodations(request):
#   accommodations = Accommodation.objects.all()
#   paginator = Paginator(accommodations, 3)
#   page_number = request.GET.get("page")
#   return paginator.get_page(page_number)
#
#def accommodations(request):
#    return render(
#        request=request,
#        context={"accommodation_list": get_accommodations(request)},
#        template_name="accommodation/accommodation_list.html",
#    )   
#
#
#def create_accommodation(request):
#   if request.method == "POST":
#       accommodation_form = AccommodationForm(request.POST)
#       if accommodation_form.is_valid():
#           data = accommodation_form.cleaned_data
#           actual_objects = Accommodation.objects.filter(
#               name=data["name"]
#           ).count()
#           print("actual_objects", actual_objects)
#           if not actual_objects:
#                accommodation = Accommodation( 
#                    name=data["name"])
#                accommodation.save()
#                messages.success(
#                    request,
#                    f"Alojamiento {data['name']} agregado exitosamente!",
#                )
#                return render(
#                    request=request,
#                    context={"accommodation_list": get_accommodations(request)},
#                    template_name="accommodation/accommodation_list.html",
#                )
#
#           else:
#            messages.error(
#                    request,
#                    f"El alojamiento {data['name']} ya está registrado",
#                )
#
#
#   accommodation_form = AccommodationForm(request.POST) 
#   context_dict = {"form": accommodation_form}
#   return render(
#       request=request,
#       context=context_dict,
#       template_name="accommodation/accommodation_form.html",
#   )
#
#def accommodation_detail(request, pk: int):
#    return render(
#        request=request,
#        context={"accommodation": Accommodation.objects.get(pk=pk)},
#        template_name="accommodation/accommodation_detail.html",
#    )
#
#
#def accommodation_update(request, pk: int):
#    accommodation = Accommodation.objects.get(pk=pk)
#
#    if request.method == "POST":
#        accommodation_form = AccommodationForm(request.POST)
#        if accommodation_form.is_valid():
#            data = accommodation_form.cleaned_data
#            accommodation.name = data["name"]
#            accommodation.location = data["location"]
#            accommodation.contact = data["contact"]
#            accommodation.price = data["price"]
#            accommodation.description = data["description"]
#            accommodation.save()
#
#            return render(
#                request=request,
#                context={"accommodation": accommodation},
#                template_name="accommodation/accommodation_detail.html",
#            )
#
#    accommodation_form = AccommodationForm(model_to_dict(accommodation))
#    context_dict = {
#        "accommodation": accommodation,
#        "form": accommodation_form,
#    }
#    return render(
#        request=request,
#        context=context_dict,
#        template_name="accommodation/accommodation_form.html",
#    )
#
#
#def accommodation_delete(request, pk: int):
#    accommodation = Accommodation.objects.get(pk=pk)
#    if request.method == "POST":
#        accommodation.delete()
#
#        accommodations = Accommodation.objects.all()
#        context_dict = {"accommodation_list": accommodations}
#        return render(
#            request=request,
#            context=context_dict,
#            template_name="accommodation/accommodation_list.html",
#        )
#
#    context_dict = {
#        "accommodation": accommodation,
#    }
#    return render(
#        request=request,
#        context=context_dict,
#        template_name="accommodation/accommodation_confirm_delete.html",
#    )
#


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
    fields = ["name","description"]

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






