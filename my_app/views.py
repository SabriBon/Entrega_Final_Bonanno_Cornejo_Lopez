from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView




from my_app.forms import DestinoForm
from my_app.models import Destino




class DestinoListView(ListView):
    model = Destino
    paginate_by = 3


class DestinoDetailView(DetailView):
    model = Destino
    template_name = "my_app/destino_detail.html"
    fields = ["name", "year", "description"]

    def get(self, request, pk):
        destino = Destino.objects.get(id=pk)
        context = {
            "destino": destino,

        }
        return render(request, self.template_name, context)   


class DestinoCreateView(LoginRequiredMixin, CreateView):
    model = Destino
    success_url = reverse_lazy("my_app:destino-list")

    form_class = DestinoForm
 

    def form_valid(self, form):
        data = form.cleaned_data
        form.instance.owner = self.request.user
        actual_objects = Destino.objects.filter(
            name=data["name"],
            year=data["year"],
        ).count()
        if actual_objects:
            messages.error(
                self.request,
                f"El destino {data['name']} ya está registrado",
            )
            form.add_error("name", ValidationError("Acción no válida"))
            return super().form_invalid(form)
        else:
            messages.success(
                self.request,
                f"Viaje {data['name']} {data['year']}  agregado exitosamente!",
            )
            return super().form_valid(form)


class DestinoUpdateView(LoginRequiredMixin, UpdateView):
    model = Destino
    fields = ["name", "year", "description","image"]

    def get_success_url(self):
        destino_id = self.kwargs["pk"]
        return reverse_lazy("my_app:destino-detail", kwargs={"pk": destino_id})


class DestinoDeleteView(LoginRequiredMixin, DeleteView):
    model = Destino
    success_url = reverse_lazy("my_app:destino-list")


