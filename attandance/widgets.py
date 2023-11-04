from django.forms.widgets import NumberInput

class MeasurementInput(NumberInput):
    template_name = 'widgets/measurement_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        # Assuming the form instance is available in widget's context under 'form'
        # Get the current value of the Measurement_unit field
        unit = self.attrs.get('data-unit', 'ft')  # Defaulting to feet
        context['widget']['unit'] = unit
        return context