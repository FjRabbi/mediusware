import json
from django.views import generic
from django.http import JsonResponse
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice
from django.db.models import Q


class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all())
        return context
    
    def post(self, request, **kwargs):
        data = json.loads(request.body)
        print(data, 'data')
        
        # saving the product 
        product = Product(title=data['title'], description=data['description'], sku=data['sku'])
        product.save()

        # saving the product image
        images = data['product_image']
        if len(images) > 0:
            for image in images:
                ProductImage(product=product.id, filepath=image).save()

        # saving the variants
        variants = data['product_variant']
        variants_count = 1
        variant_one = Variant.objects.get(id=variants[0]['option'])

        try:
            variant_two = Variant.objects.get(id=variants[1]['option'])
            variants_count += 1
        except:
            pass

        try:
            variant_three = Variant.objects.get(id=variants[2]['option'])
            variants_count += 1
        except:
            pass

        
        variant_one_list = []
        variant_two_list = []
        variant_three_list = []
        
        if variants_count == 1:
            for tag in variants[0]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_one, product=product)
                variant_one_list.append(prod_var)
                prod_var.save()

            product_variant_prices = data['product_variant_prices']

            for (index, var) in enumerate(variant_one_list):
                ProductVariantPrice(product_variant_one=var, price=product_variant_prices[index]['price'], stock=product_variant_prices[index]['stock'], product=product).save()

        elif variants_count == 2:
            for tag in variants[0]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_one, product=product)
                variant_one_list.append(prod_var)
                prod_var.save()

            for tag in variants[1]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_two, product=product)
                variant_two_list.append(prod_var)
                prod_var.save()

            product_variant_prices = data['product_variant_prices']

            index = 0
            for var in variant_one_list:
                for var2 in variant_two_list:
                    ProductVariantPrice(product_variant_one=var, product_variant_two=var2, price=product_variant_prices[index]['price'], stock=product_variant_prices[index]['stock'], product=product).save()
                    index += 1

        elif variants_count == 3:
            for tag in variants[0]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_one, product=product)
                variant_one_list.append(prod_var)
                prod_var.save()

            for tag in variants[1]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_two, product=product)
                variant_two_list.append(prod_var)
                prod_var.save()

            for tag in variants[2]['tags']:
                prod_var = ProductVariant(variant_title=tag, variant=variant_three, product=product)
                variant_three_list.append(prod_var)
                prod_var.save()

            product_variant_prices = data['product_variant_prices']
            index = 0
            for var in variant_one_list:
                for var2 in variant_two_list:
                    for var3 in variant_three_list:
                        ProductVariantPrice(product_variant_one=var, product_variant_two=var2, product_variant_three=var3, price=product_variant_prices[index]['price'], stock=product_variant_prices[index]['stock'], product=product).save()
                        index += 1

        return JsonResponse('ok', safe=False)



class ProductListView(generic.ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 2
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        print(context)

        variants = Variant.objects.prefetch_related('productvariant')
        # color = ProductVariant.objects.filter(variant__title='Color')
        # size = ProductVariant.objects.filter(variant__title='Size')
        # style = ProductVariant.objects.filter(variant__title='Style')
        context['variants'] = variants
        # context['colors'] = color
        # context['sizes'] = size
        # context['styles'] = style

        return context
    

    def get_queryset(self):
        products = super().get_queryset().prefetch_related('productvariantprice').all()

        query = self.request.GET
        print(query, 'query')
        print(self.request.get_full_path(), 'full path')
        page = query.get('page')
        print(page, 'page ---- \n\n')

        if query:
            title = query.get('title')
            price_from = query.get('price_from')
            price_to= query.get('price_to')
            date = query.get('date')
            variant = query.get('variant')
            if title:
                products = products.filter(title__icontains=title)
                print('in title --------------------')

            if price_from and price_to:
                products = products.filter(productvariantprice__price__range=(price_from, price_to)).distinct()
                print('in boht prices -----------------------------')

            elif price_from and not price_to:
                products = products.filter(productvariantprice__price__gte=price_from).distinct()
                print(len(products))
                print('in from prices --------------------------------')
            
            elif not price_from and price_to:
                products = products.filter(productvariantprice__price__lte=price_to).distinct()
                print('in to prices --------------------------------')

            if date:
                products = products.filter(productvariantprice__created_at__icontains=date).distinct()
                print('in date  --------------------------------')

            if variant:
                products = products.filter(Q(productvariantprice__product_variant_one__variant_title=variant) | Q(productvariantprice__product_variant_two__variant_title=variant) | Q(productvariantprice__product_variant_three__variant_title=variant)).distinct()
                print('in variant --------------------------------')


        print(products, 'qyersdf -----------------------------------')
        return products