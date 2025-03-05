from django import forms
from .models import Post , Comment

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("body","slug")
    


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body":forms.Textarea(attrs={"placeholder":"put your comment here","class":"form-control"})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {
            "body":forms.Textarea(attrs={"placeholder":"put your comment here","class":"form-control"})
        }


class SearchForm(forms.Form):
    search = forms.CharField(widget=(forms.TextInput(attrs={"placeholder":"Search here","class":"form-control"})))


