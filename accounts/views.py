from django.shortcuts import render
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView
from . import forms
from django.shortcuts import get_object_or_404,get_list_or_404
from django.contrib.auth import login
from .models import User
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import UserCreateForm as SignUpForm
from .tokens import account_activation_token
from blog.models import Post



# Create your views here.
class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'registration/signup.html'

from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'
    #success_url = reverse_lazy('blog:home')

# function based view to incorporate email confirmation


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = user.username
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Channel Account :)'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('accounts:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



from django.views.generic import TemplateView

class account_activation_sent(TemplateView):
    template_name = 'registration/account_activation_sent.html'




def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('accounts:activated')
    else:
        return render(request, 'registration/account_activation_invalid.html')



class activated(TemplateView):
    template_name = 'registration/successful_activation.html'


def profile_view(request,username):
    template_name = 'registration/profile.html'
    user = get_object_or_404(User, username=username)
    post = get_list_or_404(Post,author=user)
    content = {
        'user':user,
        'post':post
    }
    return render(request,template_name,content)