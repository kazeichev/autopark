from django import forms

from vehicles.models import Vehicle


class VehicleEditForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            'vehicle_brand',
            'enterprise',
            'mileage',
            'condition',
            'price',
            'purchase_date',
        ]

        labels = {
            'vehicle_brand': 'Бренд автомобиля',
            'mileage': 'Пробег',
            'purchase_date': 'Дата покупки',
            'condition': 'Состояние',
            'price': 'Цена',
            'enterprise': 'Предприятие'
        }


class VehicleCreateForm(VehicleEditForm):
    class Meta(VehicleEditForm.Meta):
        exclude = ['enterprise']
