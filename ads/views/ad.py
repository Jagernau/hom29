import json
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, UpdateView
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)

from ads.models import Ad, Category
from rest_framework.request import HttpRequest
from users.models import User

from ads.serializer import AdSerializer, AdDetailSerializer, AdCreateSerializer


class AdListView(ListAPIView):
    queryset: QuerySet[Ad] = Ad.objects.all()
    serializer_class = AdSerializer

    def get(self, request: HttpRequest, *args, **kwargs):

        categories = request.GET.getlist("cat", default=None)
        catig_qu = None
        for catig_id in categories:
            if catig_qu is None:
                catig_qu = Q(category__id__exact=catig_id)
            else:
                catig_qu |= Q(catigory__id__exact=catig_id)
        if catig_qu:
            self.queryset = self.queryset.filter(catig_qu)

        names = request.GET.get("text", default=None)
        if names:
            self.queryset = self.queryset.filter(name__icontains=names)

        locat = request.GET.get("location", default=None)
        if locat:
            self.queryset = self.queryset.filter(
                author__location__name__icontains=locat
            )

        price_from = request.GET.get("price_from", default=None)
        price_to = request.GET.get("price_to", default=None)
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer


class AdCreateView(CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "price", "description", "is_published", "image", "category"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)
        ad = self.object

        ad.name = ad_data.get("name")
        ad.price = ad_data.get("price")
        ad.description = ad_data.get("description")
        ad.is_published = ad_data.get("is_published")
        ad.category_id = ad_data.get("category_id")

        ad.save()

        response = {
            "id": ad.id,
            "author_id": ad.author_id,
            "author": str(ad.author),
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category_id": ad.category_id,
            "category": str(ad.category),
        }

        return JsonResponse(response, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad
    fields = ["name", "image"]

    def post(self, request, *args, **kwargs):

        ad = self.get_object()
        ad.image = request.FILES["image"]
        ad.save()

        response = {
            "id": ad.id,
            "author_id": ad.author_id,
            "author": str(ad.author),
            "name": ad.name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "image": ad.image.url if ad.image else None,
            "category_id": ad.category_id,
            "category": str(ad.category),
        }

        return JsonResponse(response, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "OK"}, status=200)
