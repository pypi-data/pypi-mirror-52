# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FornaContainer(Component):
    """A FornaContainer component.
This is a FornaContainer component.

Keyword arguments:
- id (string; optional): Dash-assigned id
- sequence (string; optional): The sequence
- structure (string; optional): The structure"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, sequence=Component.UNDEFINED, structure=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'sequence', 'structure']
        self._type = 'FornaContainer'
        self._namespace = 'dash_bio'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'sequence', 'structure']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(FornaContainer, self).__init__(**args)
