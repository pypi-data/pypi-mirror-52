from django import forms

from crispy_forms.helper import FormHelper

from countable_field.widgets import CountableWidget
from django.forms import TextInput, MultiWidget


class NestedFormWidget(MultiWidget):
    def __init__(self, attrs=None):
        _widgets = [
            CountableWidget(attrs={'data-max-count': 160,
                                   'data-count': 'characters',
                                   'data-count-direction': 'down'}),
            CountableWidget(attrs={'data-max-count': 160,
                                   'data-count': 'characters',
                                   'data-count-direction': 'down'})
        ]

        super(NestedFormWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        return [value.field1, value.field2] if value else [None, None]


class NestedForm(forms.MultiValueField):
    widget = NestedFormWidget

    def __init__(self, *args, **kwargs):
        list_fields = [
            forms.CharField(label="A nested field"),
            forms.CharField(label="Another nested field")
        ]
        super(NestedForm, self).__init__(
            fields=list_fields,
            require_all_fields=False, **kwargs
        )

    def compress(self, values):
        return values


class CountableTestForm(forms.Form):
    char_count_field = forms.CharField(label="Character count")
    word_count_field = forms.CharField(label="Word count")
    paragraph_count_field = forms.CharField(label="Paragraph count")
    sentence_count_field = forms.CharField(label="Sentence count")
    nested_form = NestedForm()
    # nested_form = forms.CharField(
    #     label="Nested Fields", widget=NestedFormWidget())

    def __init__(self, *args, **kwargs):
        super(CountableTestForm, self).__init__(*args, **kwargs)
        self.fields['char_count_field'].widget = CountableWidget(attrs={'data-max-count': 160,
                                                                        'data-count': 'characters',
                                                                        'data-count-direction': 'down'})
        self.fields['char_count_field'].help_text = "Type up to 160 characters"
        self.fields['word_count_field'].widget = CountableWidget(attrs={'data-min-count': 100,
                                                                        'data-max-count': 200})
        self.fields['word_count_field'].help_text = "Must be between 100 and 200 words"
        self.fields['paragraph_count_field'].widget = CountableWidget(attrs={'data-min-count': 2,
                                                                             'data-count': 'paragraphs'})
        self.fields['paragraph_count_field'].help_text = "Must be at least 2 paragraphs"
        self.fields['sentence_count_field'].widget = CountableWidget(
            attrs={'data-count': 'sentences'})

        self.helper = FormHelper()
        self.helper.wrapper_class = 'row'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.help_text_inline = False
