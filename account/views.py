from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404
from django.views import View
from .forms import RegisterForm,LoginUserForm , EditUserForm
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Relation
from .tasks import set_admin
from django.contrib.auth.mixins import UserPassesTestMixin
# Create your views here.



class LoginUserView(View):
    form_class = LoginUserForm

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get("next")
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,"account/login.html",{"form":form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"],password=cd["password"])
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully","success")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            else:
                messages.error(request,"username or password is wrong",extra_tags="danger")
                return redirect("account:login")
        return render(request,"account/login.html",{"form":form})   


class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,"Logged out successfully","success")
        return redirect("home:home")

class RegisterUserView(View):
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self,request):
        form = self.form_class()
        return render(request,"account/register.html",{"form":form})
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd["username"],cd["email"],cd["password"])
            messages.success(request,"User has been created successfully","success")
            return redirect("home:home")
        return render(request,"account/register.html",{"form":form})
    

class FollowUserView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists() or request.user == user:
            messages.error(request,"You cant follow this user","danger")
            return redirect("home:profile",user.id)
        else:
            Relation.objects.create(from_user=request.user,to_user=user)
            set_admin.delay(user.id)
            messages.success(request,"You followed this user","success")
            return redirect("home:profile",user.id)
        
class UnfollowUserView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User,id=user_id)
        relation = Relation.objects.filter(from_user=request.user,to_user=user)
        if not relation.exists() or request.user == user:
            messages.error(request,"You cant unfollowing this user","danger")
        else:
            relation.delete()
            messages.info(request,"You unfollowed this user","success")
        return redirect("home:profile",user.id)
    


class EditUserView(LoginRequiredMixin,View):
    form_class = EditUserForm
    def get(self,request):
        form  = self.form_class(instance=request.user.profile,initial={"email":request.user.email})
        return render(request,"account/edit.html",{"form":form})
    
    def post(self,request):
        form = self.form_class(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data["email"]
            request.user.save()
            messages.success(request,"profile has been edited successfully","success")
        return redirect("home:profile",request.user.id)
    