from django.db import models
from treebeard.mp_tree import MP_Node
from apps.catalog.managers import CategoryQuerySet
from apps.utils.fields import UpperCaseCharField
from apps.utils.models import AuditableModel


class Category(MP_Node):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    is_public = models.BooleanField(default=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class OptionGroup(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group"
        verbose_name_plural = "Option Groups"


class OptionGroupValue(models.Model):
    title = models.CharField(max_length=200)
    group = models.ForeignKey(OptionGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option Group Value"
        verbose_name_plural = "Option Group Values"


class ProductClass(models.Model):
    options = models.ManyToManyField('Option', blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    track_stock = models.BooleanField(default=True)
    require_shipping = models.BooleanField(default=True)

    @property
    def has_attribute(self):
        return self.attributes.exists()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Class"
        verbose_name_plural = "Product Classes"


class ProductAttribute(models.Model):
    class AttributeTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    product_class = models.ForeignKey(ProductClass, on_delete=models.CASCADE, blank=True, null=True, related_name='attributes')
    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=AttributeTypeChoice.choices, default=AttributeTypeChoice.text)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"


class Option(models.Model):
    class OptionTypeChoice(models.TextChoices):
        text = 'text'
        integer = 'integer'
        float = 'float'
        option = 'option'
        multi_option = 'multi_option'

    option_group = models.ForeignKey(OptionGroup, on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=OptionTypeChoice.choices, default=OptionTypeChoice.text)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Option"


class Product(AuditableModel):
    class ProductTypeChoice(models.TextChoices):
        standalone = 'standalone'
        parent = 'parent'
        child = 'child'

    product_class = models.ForeignKey(ProductClass, on_delete=models.PROTECT, blank=True, null=True, related_name='products')
    attributes = models.ManyToManyField(ProductAttribute, through='ProductAttributeValue')
    recommended_products = models.ManyToManyField('catalog.Product', blank=True, through='ProductRecommendation')
    categories = models.ManyToManyField(Category, related_name='categories')
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="children")
    structure = models.CharField(max_length=20, choices=ProductTypeChoice.choices, default=ProductTypeChoice.standalone)
    title = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    upc = UpperCaseCharField(max_length=20, blank=True, null=True, unique=True)
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    is_public = models.BooleanField(default=True)

    @property
    def main_image(self):
        if self.images.exists():
            return self.images.first()
        else:
            return None

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value_text = models.TextField(blank=True, null=True)
    value_integer = models.IntegerField(blank=True, null=True)
    value_float = models.FloatField(blank=True, null=True)
    value_option = models.ForeignKey(OptionGroupValue, on_delete=models.PROTECT, blank=True, null=True)
    value_multi_option = models.ManyToManyField(OptionGroupValue, blank=True, related_name='multi_valued_attribute_value')

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"
        unique_together = ['product', 'attribute']


class ProductRecommendation(models.Model):
    primary = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='primary_recommendation')
    recommendation = models.ForeignKey(Product, on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['primary', '-rank']
        unique_together = ['primary', 'recommendation']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ForeignKey('media.Image', on_delete=models.PROTECT)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order']

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        for index, image in enumerate(self.product.images.all()):
            image.display_order = index
            image.save()
