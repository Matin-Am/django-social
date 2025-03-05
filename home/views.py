from django.shortcuts import render , redirect
from django.shortcuts import get_object_or_404 
from django.views import View
from .models import Post , Comment
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostCreateForm , CommentCreateForm ,CommentReplyForm , SearchForm
from django.contrib import messages
from account.models import Relation
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from utils import IsAdminUserMixin
# Create your views here.


class HomeView(View):
    form_class = SearchForm
    def get(self,request):
        posts = Post.objects.all()
        if request.GET.get("search"):
            posts = posts.filter(body__contains=request.GET["search"])
        return render(request,"home/home.html",{"posts":posts,"form":self.form_class})
    
class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs["post_id"],slug=kwargs["slug_id"])
        return super().setup(request, *args, **kwargs)

    def get(self,request,post_id,slug_id):
        form  = self.form_class()
        comments = self.post_instance.pcomments.filter(is_reply=False)
        return render(request,"home/postdetail.html",{"post":self.post_instance,"comments":comments,"form":form,"reply_form":self.form_class_reply})
    
    @method_decorator(login_required)
    def post(self,request,post_id,slug_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = self.post_instance
            new_form.save()
            messages.success(request,"Comment has been sent successfully","success")
            return redirect("home:postdetail",self.post_instance.id,self.post_instance.slug)
        
class ProfileUserView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        is_followed = False
        user = get_object_or_404(User,pk=user_id)
        relation = Relation.objects.filter(from_user=request.user, to_user=user)
        followers = Relation.follower_count(self,user_id)
        if relation.exists():
            is_followed = True
        posts = Post.objects.filter(user=user)
        return render(request,"home/profile.html",{"posts":posts,"user":user,"is_followed":is_followed,"followers":followers})




class PostCreateView(LoginRequiredMixin,View):
    form_class = PostCreateForm

    def get(self,request):
        form = self.form_class()
        return render(request,"home/create.html",{"form":form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request,"Post has been created successfully","success")
            return redirect("home:profile",request.user.id)
        return render(request,"home/create.html",{"form":form})


class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostCreateForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post,pk=kwargs["post_id"])
        return super().setup(request, *args, **kwargs)


    def dispatch(self, request, *args, **kwargs):
        if  request.user.id != self.post_instance.user.id:
            messages.error(request,"You cant update this post","danger")
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)


    def get(self,request,post_id):
        form = self.form_class(instance=self.post_instance)
        return render(request,"home/update.html",{"form":form})
    def post(self,request,post_id):
        form = self.form_class(request.POST,instance=self.post_instance)
        if form.is_valid():
            form.save()
            messages.success(request,"Post has been successfully updated","success")
            return redirect("home:postdetail",self.post_instance.id,self.post_instance.slug)
        form = self.form_class(request.POST,instance=self.post_instance)


class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = get_object_or_404(Post,id=post_id)
        if request.user.id != post.user.id:
            messages.error(request,"You cant delete this post","danger")
            return redirect("home:home")
        else:
            post.delete()
            messages.success(request,"Post has been deleted successsfully","success")
            return redirect("home:profile",request.user.id)
        


class CommentReplyView(IsAdminUserMixin,View):
    form_class_reply =  CommentReplyForm

    def post(self,request,post_id,comment_id):
        post = get_object_or_404(Post,id=post_id)
        comment = Comment.objects.get(id=comment_id)
        form = self.form_class_reply(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.post = post
            new_form.reply = comment
            new_form.is_reply = True
            new_form.save()
            messages.success(request,"reply has beem  submitted successfully","success")
        return redirect("home:postdetail",post.id,post.slug)
    