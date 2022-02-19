from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from extra_views import CreateWithInlinesView, SearchableListMixin

from .forms import CreateItemForm, ItemImageInline, ItemLocationInline
from . import models

# Create your views here.

def index(request):
    return HttpResponse("Welcome to the ZAM Inventory Managment.")

class DetailLocationView(DetailView):
    model = models.Location
    #(request, pk, unique_identifier):
    # Prio 1
    #return HttpResponse("Here should be an overview of items stored at this location.")

    # TODO
    # * inform user, if redirect with changed unique_identifier occurred

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.unique_identifier != kwargs['unique_identifier']:
            return redirect(self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

def create_item(request):
    # Prio 0
    # get location_id from request
    context = {}
    
    item_form = CreateItemForm()
    context['form'] = item_form
    return render(request, "inventory/create_item.html", context)

def update_item(request, id):
    # Prio 3
    pass

def delete_item(request, id):
    # Prio 5
    pass

def update_location(request, pk, unique_identifier):
    # Prio 4
    pass

def view_item(request, pk):
    pass


class CreateItemView(CreateWithInlinesView):
    model = models.Item
    inlines = [ItemImageInline, ItemLocationInline]
    template_name = 'inventory/item_formset.html'
    form_class = CreateItemForm

    def get_success_url(self):
        url = reverse_lazy('create_item')

        # TODO get location from what the user entered, not was set as default
        # (may have changed)
        pass
        if self.request.GET and 'location_id' in self.request.GET:
            url += '?location_id=%s' % self.request.GET.get('location_id')

        return  url
 
 
class SearchableItemListView(SearchableListMixin, ListView):
    # matching criteria can be defined along with fields
    search_fields = ["name", "category__name"]
    search_date_fields = []
    model = models.Item
    exact_query = False
    wrong_lookup = False

    #def get_search_query(self):
    #    # Overwrite query here
    #    return super().get_search_query()
