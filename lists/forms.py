from django.core.exceptions import ValidationError
from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "Empty items will not be entered"
DUPLICATE_ITEM_ERROR = "This item is already on the list"

class ItemForm(forms.models.ModelForm):
    
    class Meta:

        model = Item
        fields = ('text',)

        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': "Enter a to-do item",
                'class': 'form-control input-lg',
            }),
        }

        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):

        # instance attr represents db object being modified/created
        self.instance.list = for_list

        return super().save()

class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        
        try: self.instance.validate_unique()

        except ValidationError as exception:
            exception.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(exception)