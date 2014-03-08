class ValidationError(Exception):
    pass


class Type(object):
    component = None
    validators = ()

    def __init__(self, label=None, help_text=None, validators=None, component=None):
        self.label = label
        self.help_text = help_text
        if validators is not None:
            self.validators = validators
        if component is not None:
            self.component = component

    def serialize(self, value):
        """
        Given a user-entered value, validator and serialize into an appropriate
        json-serializable setting.
        """
        return value


class String(Type):
    component = 'string'

    def __init__(self, max_length=None, **kwargs):
        super(String, self).__init__(**kwargs)
        self.max_length = max_length

    def serialize(self, value):
        value = unicode(value)
        if len(value) > self.max_length:
            raise ValidationError('Maximum length of value is {0}.'.format(self.max_length))
        return value


class Number(Type):
    component = 'number'

    def __init__(self, min=None, max=None, **kwargs):
        super(Number, self).__init__(**kwargs)
        self.min = min
        self.max = max

    def serialize(self, value):
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError('Value must be a number.')

        if self.min is not None and value < self.min:
            raise ValidationError('Value must be greater than or equal to {0}'.format(self.min))

        if self.max is not None and value > self.max:
            raise ValidationError('Value must be less than or equal to {0}'.format(self.max))

        return value


class Config(object):
    pass
