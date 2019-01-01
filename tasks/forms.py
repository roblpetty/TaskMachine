from django import forms
from .models import Post

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','due_date','complete','optional','content']
        labels ={'title': 'Title','due_date': 'Due Date (YYYY-MM-DD)','Has this task been completed?': 'Completed','optional': 'Is this task optional?','content': 'Content'}
    
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
        labels ={'title': 'Title','due_date': 'Due Date (YYYY-MM-DD)','complete': 'Completed? (can only be marked complete if subtasks are complete or optional)','optional': 'Is this task optional?','content': ''}

    def clean_complete(self):
        if self.instance.completable:
            return self.cleaned_data.get('complete')
        else:
            return False

    def clean(self):
        qs = Post.objects.filter(
            author=self.user, title=self.data['title']).exclude(pk=self.instance.pk)
        if qs.count() > 0:
            raise forms.ValidationError("Another task with this title already exists")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(UpdatePostForm, self).__init__(*args,**kwargs)
        if not self.instance.completable:
            self.fields['complete'].widget.attrs['readonly'] = True
            self.fields['complete'].widget.attrs['disabled'] = True
                        