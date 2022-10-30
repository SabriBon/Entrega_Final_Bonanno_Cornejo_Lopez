from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render


from accommodation.forms import AccommodationForm
from accommodation.models import Accommodation


def get_accommodations(request):
   accommodations = Accommodation.objects.all()
   paginator = Paginator(accommodations, 3)
   page_number = request.GET.get("page")
   return paginator.get_page(page_number)

def accommodations(request):
    return render(
        request=request,
        context={"accommodation_list": get_accommodations(request)},
        template_name="accommodation/accommodation_list.html",
    )   


def create_accommodation(request):
   if request.method == "POST":
       accommodation_form = AccommodationForm(request.POST)
       if accommodation_form.is_valid():
           data = accommodation_form.cleaned_data
           actual_objects = Accommodation.objects.filter(
               name=data["name"]
           ).count()
           print("actual_objects", actual_objects)
           if not actual_objects:
                accommodation = Accommodation( 
                    name=data["name"])
                accommodation.save()
                messages.success(
                    request,
                    f"Alojamiento {data['name']} agregado exitosamente!",
                )
                return render(
                    request=request,
                    context={"accommodation_list": get_accommodations(request)},
                    template_name="accommodation/accommodation_list.html",
                )

           else:
            messages.error(
                    request,
                    f"El alojamiento {data['name']} ya está registrado",
                )


   accommodation_form = AccommodationForm(request.POST) 
   context_dict = {"form": accommodation_form}
   return render(
       request=request,
       context=context_dict,
       template_name="accommodation/accommodation_form.html",
   )

def accommodation_detail(request, pk: int):
    return render(
        request=request,
        context={"accommodation": Accommodation.objects.get(pk=pk)},
        template_name="accommodation/accommodation_detail.html",
    )


def accommodation_update(request, pk: int):
    accommodation = Accommodation.objects.get(pk=pk)

    if request.method == "POST":
        accommodation_form = AccommodationForm(request.POST)
        if accommodation_form.is_valid():
            data = accommodation_form.cleaned_data
            accommodation.name = data["name"]
            accommodation.location = data["location"]
            accommodation.contact = data["contact"]
            accommodation.price = data["price"]
            accommodation.description = data["description"]
            accommodation.save()

            return render(
                request=request,
                context={"accommodation": accommodation},
                template_name="accommodation/accommodation_detail.html",
            )

    accommodation_form = AccommodationForm(model_to_dict(accommodation))
    context_dict = {
        "accommodation": accommodation,
        "form": accommodation_form,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="accommodation/accommodation_form.html",
    )


def accommodation_delete(request, pk: int):
    accommodation = Accommodation.objects.get(pk=pk)
    if request.method == "POST":
        accommodation.delete()

        accommodations = Accommodation.objects.all()
        context_dict = {"accommodation_list": accommodations}
        return render(
            request=request,
            context=context_dict,
            template_name="accommodation/accommodation_list.html",
        )

    context_dict = {
        "accommodation": accommodation,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="accommodation/accommodation_confirm_delete.html",
    )

from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from accommodation.models import Accommodation


class AccommodationListView(ListView):
    model = Accommodation
    paginate_by = 3


class AccommodationDetailView(DetailView):
    model = Accommodation
    fields = ["name", "location","contact","price", "description"]


class AccommodationCreateView(CreateView):
    model = Accommodation
    success_url = reverse_lazy("accommodation:accommodation-list")

    form_class = AccommodationForm
    fields = ["name", "location","contact","price", "description"]

    def form_valid(self, form):
        """Filter to avoid duplicate accommodations"""
        data = form.cleaned_data
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


class AccommodationUpdateView(UpdateView):
    model = Accommodation
    fields = ["name", "location", "description"]

    def get_success_url(self):
        accommodation_id = self.kwargs["pk"]
        return reverse_lazy("accommodation:accommodation-detail", kwargs={"pk": accommodation_id})


class AccommodationDeleteView(DeleteView):
    model = Accommodation
    success_url = reverse_lazy("accommodation:accommodation-list")







