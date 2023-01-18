from django.db import models
from config.g_model import TimeStampMixin


# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    # @property
    # def get_prod_var_prices(self, price_from=None, price_to=None, date=None):
    #     if price_from == None and price_to == None and date == None:
    #         prod_variant_prices = self.productvariantprice_set.all()
    #     elif price_from and price_to:
    #         prod_variant_prices = self.productvariantprice_set.filter(price__range=(price_from, price_to))
    #     # elif price_from and price_to == None:
    #     #     prod_variant_prices = self.productvariantprice_set.filter(price__range=(price_from, price_to))

    #     return prod_variant_prices

    # @property

class ProductImage(TimeStampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.URLField()


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='productvariant')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class ProductVariantPrice(TimeStampMixin):
    product_variant_one = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price = models.FloatField()
    stock = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='productvariantprice')