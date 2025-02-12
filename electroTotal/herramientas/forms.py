from django import forms

class PDFUploadForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'custom-input form-control'
        })
    )
    # Aunque definimos el campo, en la plantilla mostraremos el control de color de forma personalizada.
    color_mode = forms.ChoiceField(
        choices=[('color', 'Color'), ('grayscale', 'Blanco y Negro')],
        required=True,
        label="Modo de color",
        widget=forms.RadioSelect()  # Este widget no se usará directamente en la plantilla.
    )
    dpi = forms.IntegerField(
        initial=300,
        min_value=100,
        max_value=600,
        required=True,
        label="Resolución (DPI)",
        widget=forms.NumberInput(attrs={
            'class': 'custom-range',
            'type': 'range',
            'min': '100',
            'max': '600',
            'value': '300'
        })
    )
    denoise = forms.BooleanField(
        required=False,
        initial=False,
        label="Reducir ruido",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
