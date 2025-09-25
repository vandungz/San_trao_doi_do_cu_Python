from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Listing, ListingImage
from .forms import ListingForm
from django.http import HttpResponseForbidden

class ListingListView(ListView):
    model = Listing
    template_name = "listings/list.html"
    context_object_name = "items"
    queryset = Listing.objects.filter(status="PUBLISHED").order_by("-created_at")


class ListingDetailView(DetailView):
    model = Listing
    template_name = "listings/detail.html"
    context_object_name = "item"


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "listings/create.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        obj.save()
        for f in self.request.FILES.getlist("images"):
            ListingImage.objects.create(listing=obj, image=f)
        return redirect(obj.get_absolute_url())


class ListingUpdateView(LoginRequiredMixin, UpdateView):
    model = Listing
    form_class = ListingForm
    template_name = "listings/edit.html"

    def form_valid(self, form):
        obj = form.save()
        for f in self.request.FILES.getlist("images"):
            ListingImage.objects.create(listing=obj, image=f)
        return redirect(obj.get_absolute_url())


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(ListingImage, id=image_id)
    listing = image.listing
    if request.user == listing.owner or request.user.is_staff:
        image.delete()
    else:
        return HttpResponseForbidden("Bạn không có quyền xóa ảnh này.")
    return redirect("listings:edit", pk=listing.pk)


@login_required
def my_listings(request):
    items = Listing.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "listings/mine.html", {"items": items})


class ListingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Listing
    template_name = "listings/confirm_delete.html"
    success_url = reverse_lazy("listings:list")

    def test_func(self):
        return self.get_object().owner == self.request.user
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_staff)  # chỉ admin/staff mới được duyệt
def publish_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.status = "PUBLISHED"
    listing.save()
    return redirect("listings:detail", pk=listing.pk)