from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, LogoutView, LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.http import HttpResponse
from django.core.paginator import Paginator
from .forms import CustomAuthenticationForm, AvatarForm, MessageForm
from .models import Avatar, Message


import json

# _____________________ AUTH VIEWS _____________________
class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView):
    template_name="users/change_password.html"
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        form.save()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "navbarChanged": None,
                    "showMessage": "La contraseña se actualizó correctamente."
                })
            }
        )


class CustomLogoutView(LogoutView):
    template_name = "products/index.html"

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return redirect ('products:index')    


# _____________________ AVATAR VIEWS _____________________

class AvatarDetailView(DetailView, LoginRequiredMixin):
    model = Avatar
    


class AvatarCreateView(View):
    def get(self, request):
        form = AvatarForm()
        return render(request, 'users/avatar_form.html', {'form': form})

    def post(self, request):
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            Avatar.objects.create(
                user=request.user,
                image=form.cleaned_data.get('image'),
            )
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "navbarChanged": None,
                        "showMessage": "El Avatar se guardó correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/avatar_form.html', {'form': form})

class AvatarConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        return render(request, 'users/avatar_confirm_action.html', {'avatar': avatar})
    


class AvatarUpdateView(View, LoginRequiredMixin):
    def get(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        form = AvatarForm(instance=avatar)
        return render(request, 'users/avatar_form.html', {'form': form, 'avatar': avatar})

    def post(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            avatar.image = form.cleaned_data.get('image')
            avatar.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "navbarChanged": None,
                        "showMessage": "El avatar se actualizó correctamente."
                    })
                }
            )
        else:
            return render(request, 'blog/post_form.html', {'form': form, 'avatar': avatar})


class AvatarDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        avatar = get_object_or_404(Avatar, pk=pk)
        avatar.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "navbarChanged": None,
                    "showMessage":"El avatar se eliminó correctamente."
                })
            }
        )


# _____________________ MESSAGE VIEWS _____________________

class MessageListView(View, LoginRequiredMixin):
    def get(self, request):
        return render(request, 'users/message_list.html', {})


class LoadMessageListView(View, LoginRequiredMixin):
    def get(self, request):
        consult = request.GET.get("consult", "")
        messages = Message.objects.filter(Q(name__icontains=consult) | Q(email__icontains=consult)).order_by("-id")
      
        paginator = Paginator(messages, 10)
        page = request.GET.get('page')
        messages = paginator.get_page(page)

        context = {
            'object_list': messages,
            'consult': consult,
        }
        return render(request, 'users/partials/message_list.html', context)
    

class MessageDetailView(View, LoginRequiredMixin):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
       
        return render(request, 'users/message_detail.html', {'message': message})
    
    def post(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.is_read = True
        message.save()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                })
            }
        )


class MessageCreateView(View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'users/message_form.html', {'form': form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                name=form.cleaned_data.get('name'),
                email=form.cleaned_data.get('email'),
                phone=form.cleaned_data.get("phone"),
                content=form.cleaned_data.get('content'),
            )
            return HttpResponse(
                status=201,
                headers={
                    'HX-Trigger': json.dumps({
                        "messageListChanged": None,
                        "showMessage": "El mensaje se envió correctamente."
                    })
                }
            )
        else:
            return render(request, 'users/message_form.html', {'form': form})


class MessageConfirmActionView(View, LoginRequiredMixin):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        return render(request, 'users/message_confirm_action.html', {'message': message})
    

class MessageUpdateView(View, LoginRequiredMixin):
    def patch(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        if message.is_read:
            message.is_read = False
            message_status = "El mensaje se marcó como no leido."
        else:
            message.is_read = True
            message_status = "El mensaje se marcó como leido."
        message.save()
        return HttpResponse(
            status=200,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                    "showMessage": message_status
                })
            }
        )
    

class MessageDeleteView(View, LoginRequiredMixin):
    def delete(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        message.delete()
        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                    "messageListChanged": None,
                    "showMessage":"El mensaje se eliminó correctamente."
                })
            }
        )
    
