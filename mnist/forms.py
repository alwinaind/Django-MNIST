from django import forms

class ImageData(forms.Form):
    image = forms.CharField(
        widget=forms.TextInput(
            attrs={'id': 'img'}))