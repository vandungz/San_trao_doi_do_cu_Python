from django import forms
from django.utils.html import escape


class MessageForm(forms.Form):
    body = forms.CharField(
        label="Tin nhan",
        min_length=1,
        max_length=2000,
        strip=True,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Nhap tin nhan...",
                "maxlength": "2000",
            }
        ),
    )

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if not body:
            raise forms.ValidationError("Noi dung khong duoc de trong.")
        return escape(body)
