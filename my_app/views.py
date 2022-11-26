from django.contrib import messages
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from my_app.forms import ViajeForm
from my_app.models import Viaje


def get_destinos(request):
   destinos = Viaje.objects.all()
   paginator = Paginator(destinos, 3)
   page_number = request.GET.get("page")
   return paginator.get_page(page_number)

def destinos(request):
    return render(
        request=request,
        context={"destino_list": get_destinos(request)},
        template_name="my_app/destino_list.html",
    )

def create_destino(request):
   if request.method == "POST":
       destino_form = ViajeForm(request.POST)
       if destino_form.is_valid():
           data = destino_form.cleaned_data
           actual_objects = Viaje.objects.filter(
               name=data["name"],
               year=data["year"],
           ).count()
           print("actual_objects", actual_objects)
           if not actual_objects:
                destino = Viaje( 
                    name=data["name"],
                    year=data["year"],)
                destino.save()
                messages.success(
                    request,
                    f"Viaje a {data['name']} en {data['year']} agregado exitosamente!",
                )
                return render(
                    request=request,
                    context={"destino_list": get_destinos(request)},
                    template_name="my_app/destino_list.html",
                )

           else:
            messages.error(
                    request,
                    f"El viaje {data['name']} ya está ingresado.",
                )


   destino_form = ViajeForm(request.POST) 
   context_dict = {"form": destino_form}
   return render(
       request=request,
       context=context_dict,
       template_name="my_app/destino_form.html",
   )

def destino_detail(request, pk: int):
    return render(
        request=request,
        context={"destino": Viaje.objects.get(pk=pk)},
        template_name="my_app/destino_detail.html",
    )


def destino_update(request, pk: int):
    destino = Viaje.objects.get(pk=pk)

    if request.method == "POST":
        destino_form = ViajeForm(request.POST)
        if destino_form.is_valid():
            data = destino_form.cleaned_data
            destino.name = data["name"]
            destino.year = data["year"]
            destino.description = data["description"]
            destino.save()

            return render(
                request=request,
                context={"destino": destino},
                template_name="my_app/destino_detail.html",
            )

    destino_form = ViajeForm(model_to_dict(destino))
    context_dict = {
        "destino": destino,
        "form": destino_form,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="my_app/destino_form.html",
    )


def destino_delete(request, pk: int):
    destino = Viaje.objects.get(pk=pk)
    if request.method == "POST":
        destino.delete()

        destinos = Viaje.objects.all()
        context_dict = {"destino_list": destinos}
        return render(
            request=request,
            context=context_dict,
            template_name="my_app/destino_list.html",
        )

    context_dict = {
        "destino": destino,
    }
    return render(
        request=request,
        context=context_dict,
        template_name="my_app/destino_confirm_delete.html",
    )

class ViajeListView(ListView):
    model = Viaje
    paginate_by = 3


class ViajeDetailView(DetailView):
    model = Viaje
    fields = ["name", "year", "description"]


class ViajeCreateView(CreateView):
    model = Viaje
    success_url = reverse_lazy("my_app:destino-list")

    form_class = ViajeForm
    fields = ["name", "year", "description"]

    def form_valid(self, form):
        """Filter to avoid duplicate destinos"""
        data = form.cleaned_data
        actual_objects = Viaje.objects.filter(
            name=data["name"],
            year=data["year"],
        ).count()
        if actual_objects:
            messages.error(
                self.request,
                f"El viaje {data['name']} ya está registrado",
            )
            form.add_error("name", ValidationError("Acción no válida"))
            return super().form_invalid(form)
        else:
            messages.success(
                self.request,
                f"Viaje {data['name']} agregado exitosamente!",
            )
            return super().form_valid(form)


class ViajeUpdateView(UpdateView):
    model = Viaje
    fields = ["name", "year", "description"]

    def get_success_url(self):
        destino_id = self.kwargs["pk"]
        return reverse_lazy("my_app:destino-detail", kwargs={"pk": destino_id})


class ViajeDeleteView(DeleteView):
    model = Viaje
    success_url = reverse_lazy("my_app:destino-list")





