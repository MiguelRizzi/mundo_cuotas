import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import DetailView
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import File, Product, Category
from .forms import ProductForm


# _____________________ CONTACT VIEW _____________________


class ContactView(View):
    def get(self, request):
        return render(request, "products/contact.html")
    
class AboutView(View):
    def get(self, request):
        return render(request, "products/about.html")

    
class IndexView(View):
    def get(self, request):
        consult = request.GET.get("consult", "").strip()

        products= Product.objects.all().exclude(status=1)
        regular_products= products.filter(type=1).order_by("-id")[:4]
        offer_products= products.filter(type=2).order_by("-id")[:4]
        featured_products= products.filter(type=3).order_by("-id")[:4]

        context = {
            "consult": consult,
            "regular_products": regular_products,
            "offer_products": offer_products,
            "featured_products": featured_products,
            "site_name": "Comprá en cuotas sin complicaciones"
        }

        return render(request, "products/index.html", context)
# _____________________ PRODUCT VIEWS _____________________

class ProductListView(View):
    def get(self, request):
        consult = request.GET.get("consult", "").strip()

        categories= Category.objects.all().order_by("name")
        products= Product.objects.all().exclude(status=1)
        regular_products= products.filter(type=1).order_by("-id")[:4]
        offer_products= products.filter(type=2).order_by("-id")[:4]
        featured_products= products.filter(type=3).order_by("-id")[:4]

        context = {
            "consult": consult,
            "categories": categories,
            "regular_products": regular_products,
            "offer_products": offer_products,
            "featured_products": featured_products,
            "site_name": "Catalogo Online"
        }

        return render(request, "products/product_list.html", context)
    
class LoadProductListView(View):
    def get(self, request):
        consult = request.GET.get("consult", "").strip()
        type = request.GET.get("type", "")
        category= request.GET.get("category", "")
        date= request.GET.get("date", "")
        
        products = Product.objects.all().exclude(status=1)
        category_object = Category.objects.filter(slug=category).first()


        consult_words = consult.split(" ")
        if consult:
            query = Q()
            for word in consult_words:
                query |= Q(name__icontains=word) | Q(category__name__icontains=word) | Q(category__parent__name__icontains=word)
            products = products.filter(query)
            
        if type:
            if type == "4":
                pass
            else:
                products = products.filter(type=type)

        if category:
            products = products.filter(category__slug__icontains=category)

        if date:
            if date == "2":
                products = products.order_by("id")
        else:
            products = products.order_by("-id")

        
        paginator = Paginator(products, 12)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {
            "object_list": products,
            "consult": consult,
            "category_object": category_object,
            "type": type,
        }
        return render(request, 'products/partials/product_list.html', context)
    
class ProductDetailView(DetailView):
    model = Product
    template_name="products/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        related_products = similar_products = Product.objects.filter(category=product.category).exclude(id=product.id).exclude(status=1)[:4] # Filtrar productos de la misma categoría excluyendo el producto actual
        context["related_products"] = related_products
        context['site_name'] = product.name
        return context
    

# _____________________ ADMIN VIEWS _____________________

    
class ProductListAdminView(View, LoginRequiredMixin):
    def get(self, request):
        categories= Category.objects.all().order_by("name")

        context = {
            'categories': categories,
            "site_name": "Administrar Catalogo Online",
        }

        return render(request, "products/products_admin.html", context)

    
class LoadProductListAdminView(View, LoginRequiredMixin):
    def get(self, request):
        consult = request.GET.get("consult", "").strip()
        status = request.GET.getlist("status", "")
        type = request.GET.getlist("type", "")
        category= request.GET.getlist("category", "")
        date= request.GET.get("date", "")
        
        products = Product.objects.all()

        consult_words = consult.split(" ")
        if consult:
            query = Q()
            for word in consult_words:
                query |= Q(name__icontains=word) | Q(category__name__icontains=word) | Q(category__parent__name__icontains=word)
            products = products.filter(query)

        if status:
            products = products.filter(status__in=status)

        if type:
            products = products.filter(type__in=type)

        if category:
            products = products.filter(category__slug__in=category)

        if date:
            if date == "2":
                products = products.order_by("id")
        else:
            products = products.order_by("-id")

        
        paginator = Paginator(products, 15)
        page = request.GET.get('page')
        products = paginator.get_page(page)

        context = {
            'object_list': products,
        }
        return render(request, 'products/partials/product_list_admin.html', context)


class ProductDetailAdminView(DetailView, LoginRequiredMixin):
    model = Product
    template_name = 'products/product_detail_admin.html'


class ProductCreateView(View, LoginRequiredMixin):
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
        subcategory= get_object_or_404(Category, id=subcategory_value)

        if form.is_valid():
            product = form.save(commit=False)
            product.category = subcategory
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
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(instance=product)

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
        product = get_object_or_404(Product, slug=slug)
        form = ProductForm(request.POST, instance=product)
        subcategory_value = request.POST.get('subcategory')
        delete_files = request.POST.getlist('delete-files')
        subcategory= get_object_or_404(Category, id=subcategory_value)

        category_field = request.POST.get('category', None)
        if not category_field:
            form.add_error(None, 'Error message for custom_field')  # Agrega un error al formulario en general


        if form.is_valid():
            product = form.save(commit=False)
            product.category = subcategory
            product.save()
            
            for file_id in delete_files:
                file = get_object_or_404(File, id=file_id)
                file.delete()
                
            for file in request.FILES.getlist('files'):
                if not File.objects.filter(product=product, file__icontains=file.name).exists():
                    file_obj = File.objects.create(file=file, product=product)
                    file_obj.save()

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
    
# _____________________ AUXILIARY VIEWS product form _____________________

class LoadSubcategoriesView(View, LoginRequiredMixin):

    def get(self, request):
        category = request.GET.get("category", "")
        if category:
            subcategories = Category.objects.filter(parent=category)
        else:
            subcategories = Category.objects.none() 

        return render(request, 'products/partials/load_subcategories.html', {'subcategories': subcategories})
    

class LoadProductSubcategoriesView(View, LoginRequiredMixin):

    def get(self, request, slug):
        category = request.GET.get("category", "")
        if category:
            subcategories = Category.objects.filter(parent=category)
        else:
            subcategories = Category.objects.none() 

        product = Product.objects.get(slug=slug)

        context={
            'subcategories': subcategories,
            'product': product
        }

        return render(request, 'products/partials/load_subcategories.html', context)
    