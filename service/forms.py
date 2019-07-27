from django import forms

from service.models import Order

class OrderCreation(forms.ModelForm):
    class Meta:
        model=Order
        fields=('type','trans_id','character_id')
        labels={'type':'UC Category',
                'trans_id':'PayTM Transaction id',
                'character_id':'Pubg Charatcter ID',
                
            }

class OrderUpdate(forms.ModelForm):
    class Meta:
        model=Order
        fields=('status',)
        