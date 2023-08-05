"""Module to provide read access to static content."""

from roax.resource import Resource, operation


class StaticResource(Resource):
    """A resource that serves static content."""

    def __init__(self, content, schema, name=None, description=None, security=None):
        """
        Initialize the static resource.

        :param content: Static content to return in a read operation.
        :param schema: Schema of the static content.
        :param name: Short name of the resource.
        :param description: Short description of the resource.
        :param security: Security requirements to read the resource.
        """
        super().__init__(name, description)
        self.content = content
        self.schema = schema
        description = f"Read the {self.name} resource."
        self.read = operation(
            params={}, returns=self.schema, description=description, security=security
        )(self.read)

    def read(self):
        """Read the static resource."""
        return self.content
