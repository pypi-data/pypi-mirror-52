__all__ = ['BaseSchema']

from marshmallow import Schema, fields, post_load


class BaseSchema(Schema):
    """Base class for use in schema'd objects

    Subclasses :any:Schema from marshmallow and provides """
    _key = fields.String()

    model_class = None

    @post_load
    def make_model(self, data):
        """Return an instance of :py:attr:model_class

        If :py:attr:model_class is :any:None, the data passed is
        returned unchanged

        :param data: Instance data
        :return:
        """
        if self.model_class is None:
            return data
        return self.model_class(**data)
