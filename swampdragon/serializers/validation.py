class ValidationError(Exception):
    def __init__(self, errors={}, *args, **kwargs):
        super(ValidationError, self).__init__(*args, **kwargs)
        self.errors = errors

    def get_error_dict(self):
        return self.errors


class ModelValidationError(ValidationError):
    pass
    # def __init__(self, errors={}, *args, **kwargs):
    #     super(ModelValidationError, self).__init__(*args, **kwargs)
    #     self.errors = errors
    #
    # def get_error_dict(self):
    #     return self.errors
