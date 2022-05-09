from django import forms
from .models import Language, LingueeLanguages


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ["src_lang", "tar_text"]
        widgets = {
            "src_text": forms.Textarea(attrs={"cols": 40, "rows": 10}),
        }


class LingueeSourceForm(forms.Form):
    source_text = forms.CharField(
        label="Source Text",
        max_length=2048,
        required=True,
        widget=forms.Textarea(attrs={"cols": 40, "rows": 10}),
    )
    dst_lang = forms.ChoiceField(
        label="Destination Language", choices=LingueeLanguages.choices
    )
