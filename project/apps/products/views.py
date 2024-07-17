import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView

from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import File, Product, Category
from .forms import ProductForm, ProductUpdateForm
from users.forms import MessageForm

from django.core.files.storage import default_storage
# _____________________ INDEX VIEW _____________________

class IndexView(View):
    def get(self, request):
        products= Product.objects.all()
        regular_products= products.filter(type=1).order_by("-id")[:4]
        offer_products= products.filter(type=2).order_by("-id")[:4]
        featured_products= products.filter(type=3).order_by("-id")[:4]

        context = {
            "regular_products": regular_products,
            "offer_products": offer_products,
            "featured_products": featured_products,
            "site_name": "Compras en cuotas a sola firma"
        }

        return render(request, "products/index.html", context)
    

class ContactView(View):
    def get(self, request):
        return render(request, "products/contact.html")

    

# _____________________ PRODUCT VIEWS _____________________

class ProductListView(View):
    def get(self, request):
        categories= Category.objects.all()

        context = {
            'categories': categories,
            "site_name": "Catalogo Online",
        }

        return render(request, "products/products.html", context)
    
class LoadProductListView(View):
    def get(self, request):
        consult = request.GET.get("consult", "")
        type = request.GET.getlist("type", "")
        category= request.GET.getlist("category", "")
        
        products = Product.objects.all().exclude(status=1)

        if consult:
            products = products.filter(name__icontains=consult)

        if type:
            products = products.filter(type__in=type)

        if category:
            products = products.filter(category__slug__in=category)

    
        products = products.order_by("-id")

        
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {
            'object_list': products,
        }
        return render(request, 'products/partials/product_list.html', context)
    

    
class ProductListAdminView(View, LoginRequiredMixin):
    def get(self, request):
        categories= Category.objects.all()

        context = {
            'categories': categories,
            "site_name": "Administrar Catalogo Online",
        }

        return render(request, "products/products_admin.html", context)

    
class LoadProductListAdminView(View, LoginRequiredMixin):
    def get(self, request):
        consult = request.GET.get("consult", "")
        status = request.GET.getlist("status", "")
        type = request.GET.getlist("type", "")
        category= request.GET.getlist("category", "")
        date= request.GET.get("date", "")
        
        products = Product.objects.all()

        if consult:
            products = products.filter(name__icontains=consult)

        if status:
            products = products.filter(status__in=status)

        if type:
            products = products.filter(type__in=type)

        if category:
            products = products.filter(category__slug__in=category)

        if date:
            if date == "1":
                products = products.order_by("-created_at")
            else:
                products = products.order_by("created_at")
        else:
            products = products.order_by("-id")

        
        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {
            'object_list': products,
        }
        return render(request, 'products/partials/product_list_admin.html', context)

    

class ProductListByCategoryView(View):
    def get(self, request, slug):
        categories= Category.objects.all()
        category= Category.objects.filter(slug=slug).first()

        context = {
            "category": category,
            "categories": categories,
            "site_name": f"Catalogo Online - {category.name}",
        }

        return render(request, "products/products_by_category.html", context)


class LoadProductListByCategoryView(View):
    def get(self, request, slug):
        consult = request.GET.get("consult", "")
        category= Category.objects.filter(slug=slug).first()
        products = Product.objects.filter(category=category).order_by("-id")

        if consult:
            products = products.filter(name__icontains=consult).order_by("-id")

        paginator = Paginator(products, 10)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {
            'object_list': products,
            "category": category,
        }

        return render(request, 'products/partials/product_list.html', context)
       

class ProductDetailView(DetailView):
    template_name = 'default_template.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]  # Filtrar productos de la misma categoría excluyendo el producto actual
        context["related_products"] = related_products
        context['site_name'] = product.name
        return context
    

class ProductCreateView(View):
    def get(self, request):
        form = ProductForm()
        categories = Category.objects.filter(parent=None)
        context = { 
            'form': form,
            'categories': categories
        }

        return render(request, 'products/product_form.html', context)

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        subcategory_value = request.POST.get('subcategory')
        subcategory= get_object_or_404(Category, slug=subcategory_value)

        if form.is_valid():
            product = Product(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=subcategory,
                type=form.cleaned_data['type'],
                status=form.cleaned_data['status'],
                price=form.cleaned_data['price'],
            )
            product.save()
            for file in request.FILES.getlist('files'):
                file_obj = File.objects.create(file=file, product=product)
                file_obj.save()
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "productListChanged": None,
                        "showMessage": "El producto se guardó correctamente."
                    })
                }
            )
        else:
            return render(request, 'products/product_form.html', {'form': form})



class ProductConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'products/product_confirm_action.html', {'product': product})
    

class ProductUpdateView(View, LoginRequiredMixin):
# Dentro de tu ProductUpdateView
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductUpdateForm(instance=product)

        subcategories = Category.objects.filter(parent=product.category)

    
        categories = Category.objects.filter(parent=None)
        categorie_value = product.category
        context = {
            "form": form,
            "product": product,
            "categories": categories,
            "subcategories": subcategories,
            "category_value": categorie_value
        }
        return render(request, 'products/product_form.html', context)

    def post(self, request, slug):
        form = ProductUpdateForm(request.POST, instance=product)
        product = get_object_or_404(Product, slug=slug)
        subcategory_value = request.POST.get('subcategory')
        subcategory= get_object_or_404(Category, slug=subcategory_value)
        if form.is_valid():
            product = Product(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                category=subcategory,
                type=form.cleaned_data['type'],
                status=form.cleaned_data['status'],
                price=form.cleaned_data['price'],
            )
            product.save()            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "productListChanged": None,
                        "showMessage": "El articulo se actualizó correctamente."
                    })
                }
            )
        else:
            return render(request, 'products/product_form.html', {'form': form, 'product': product})
    

class ProductDeleteView(View, LoginRequiredMixin):
    def delete(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        product.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "productListChanged": None,
                    "showMessage":"El producto se eliminó correctamente."
                })
            }
        )
    



class LoadSubcategoriesView(View):

    def get(self, request):
        category = request.GET.get("category", "")
        subcategories = Category.objects.filter(parent=category)
        return render(request, 'products/partials/load_subcategories.html', {'subcategories': subcategories})
    