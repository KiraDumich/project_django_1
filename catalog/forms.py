from django import forms
from catalog.models import Product


class StyleFormMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(forms.ModelForm, StyleFormMixin):

    class Meta:
        model = Product
        fields = ('name', 'description', 'cost', 'category', 'preview')

    def clean_title(self):
        cleaned_data = self.cleaned_data['name']
        for i in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']:

            if i in cleaned_data:
                raise forms.ValidationError('Название содержит запрещенные слова')

        return cleaned_data

    def clean_description(self):
        cleaned_description = self.cleaned_data['description']
        for i in ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']:

            if i in cleaned_description:
                raise forms.ValidationError('Описание товара содержит запрещенные слова')


