from django.contrib import admin
from django.db.models import Count
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
from apps.catalog.models import (
    Category, ProductClass, Option, ProductAttribute,
    ProductRecommendation, Product, ProductAttributeValue,
    ProductImage, OptionGroup, OptionGroupValue
)


# ======================================================================
@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)
    list_display = ['title', 'slug', 'description', 'is_public', 'depth', 'numchild']
    list_filter = ['is_public']
    search_fields = ['title']


class OptionGroupValueInline(admin.StackedInline):
    model = OptionGroupValue
    extra = 0
    classes = ['collapse']
    show_change_link = True


@admin.register(OptionGroup)
class OptionGroupAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    inlines = [OptionGroupValueInline]


@admin.register(OptionGroupValue)
class OptionGroupValueAdmin(admin.ModelAdmin):
    list_display = ['title', 'group']
    search_fields = ['title']
    raw_id_fields = ['group']


# ======================================================================


class ProductAttributeInline(admin.StackedInline):
    model = ProductAttribute
    extra = 0
    classes = ['collapse']
    show_change_link = True
    raw_id_fields = ['option_group']


class AttributeCountFilter(admin.SimpleListFilter):
    title = 'Attribute Count'
    parameter_name = 'attr_count'

    def lookups(self, request, model_admin):
        return [
            ('more_5', 'More Than 5'),
            ('lower_5', 'lower Than 5'),
        ]

    def queryset(self, request, queryset):
        if self.value() == "more_5":
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__gt=5)
        if self.value() == "lower_5":
            return queryset.annotate(attr_count=Count('attributes')).filter(attr_count__lte=5)


@admin.register(ProductClass)
class ProductClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'track_stock', 'require_shipping', 'attribute_count']
    list_filter = ['track_stock', 'require_shipping', AttributeCountFilter]
    search_fields = ['title']
    inlines = [ProductAttributeInline]
    actions = ['enable_track_stock']

    def attribute_count(self, obj):
        return obj.attributes.count()

    def enable_track_stock(self, request, queryset):
        queryset.update(track_stock=True)


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ['product_class', 'option_group', 'title', 'type', 'required']
    list_filter = ['required']
    search_fields = ['title']
    raw_id_fields = ['product_class', 'option_group']


# ======================================================================


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ['option_group', 'title', 'type', 'required']
    list_filter = ['required']
    search_fields = ['title']
    raw_id_fields = ['option_group']


class ProductAttributeValueInline(admin.StackedInline):
    model = ProductAttributeValue
    extra = 0
    classes = ['collapse']
    show_change_link = True
    raw_id_fields = ['attribute', 'value_option', 'value_multi_option']


class ProductRecommendationInline(admin.StackedInline):
    model = ProductRecommendation
    extra = 0
    fk_name = 'primary'
    classes = ['collapse']
    show_change_link = True
    raw_id_fields = ['primary', 'recommendation']


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    classes = ['collapse']
    show_change_link = True
    raw_id_fields = ['image']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_class', 'parent', 'structure', 'title', 'is_public']
    list_filter = ['is_public']
    search_fields = ['title']
    raw_id_fields = ['product_class', 'parent']
    inlines = [ProductAttributeValueInline, ProductRecommendationInline, ProductImageInline]


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ['product', 'attribute']
    raw_id_fields = ['product', 'attribute', 'value_option', 'value_multi_option']


@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ['primary', 'recommendation', 'rank']
    raw_id_fields = ['primary', 'recommendation']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'display_order']
    raw_id_fields = ['product', 'image']
# ======================================================================
