from rest_framework import serializers
from ads.models import Ad, Category, Location
from users.models import User
from rest_framework.generics import get_object_or_404



class LocatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=False, queryset=Category.objects.all(), slug_field="name"
    )

    author = serializers.SlugRelatedField(
        required=False, queryset=User.objects.all(), slug_field="username"
    )

    class Meta:
        model = Ad
        fields = "__all__"


class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False, read_only=True, slug_field="username"
    )

    category = serializers.SlugRelatedField(
        required=False, read_only=True, slug_field="name"
    )

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = serializers.ImageField(required=False)

    author = serializers.SlugRelatedField(
        required=False, queryset=User.objects.all(), slug_field="username"
    )
    category = serializers.SlugRelatedField(
        required=False, queryset=Category.objects.all(), slug_field="name"
    )

    class Meta:
        model = Ad
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._author_id = self.initial_data.pop("author_id")
        self._category_id = self.initial_data.pop("category_id")
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        ad = Ad.objects.create(
            name=validated_data.get("name"),
            price=validated_data.get("price"),
            description=validated_data.get("description"),
            is_published=validated_data.get("is_published"),
        )
        ad.author = get_object_or_404(User, pk=self._author_id)
        ad.category = get_object_or_404(Category, pk=self._category_id)
        ad.save()

        return ad
