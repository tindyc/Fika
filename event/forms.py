from .models import EventPost
from django import forms


class RegisterEventPostForm(forms.ModelForm):
    title = forms.CharField(max_length=75, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={"class": "form-control"}))
    

    class Meta:
        model = EventPost
        fields = (
            "title",
            "content",
            "address",
        )

    def __init__(self, *args, **kwargs):
        super(RegisterEventPostForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["content"].widget.attrs["class"] = "form-control"
        self.fields["address"].widget.attrs["class"] = "form-control"

