from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','due_date','complete','optional','content']
        labels ={'title': 'Title','due_date': 'Due Date','complete': 'Completed','optional': 'Is this task optional?','content': 'Content'}
    
    def clean(self):
        if Post.objects.filter(author=self.user,title=self.data['title']).exists():
            raise forms.ValidationError("A task with this title already exists")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(CreatePostForm, self).__init__(*args,**kwargs)

class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','due_date','complete','optional','content']
        labels ={'title': 'Title','due_date': 'Due Date (YYYY-MM-DD)','complete': 'Has this been completed','optional': 'Is this task optional?','content': ''}
    
    def clean(self):
        print(self.instance.pk)
        qs = Post.objects.filter(
            author=self.user, title=self.data['title']).exclude(pk=self.instance.pk)
        print(qs.count())
        if qs.count() > 0:
            raise forms.ValidationError("Another task with this title already exists")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdatePostForm, self).__init__(*args,**kwargs)