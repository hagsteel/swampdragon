class ModelValidationError(Exception):
    def __init__(self, errors={}, *args, **kwargs):
        super(ModelValidationError, self).__init__(*args, **kwargs)
        self.errors = errors

    def get_error_dict(self):
        return self.errors
