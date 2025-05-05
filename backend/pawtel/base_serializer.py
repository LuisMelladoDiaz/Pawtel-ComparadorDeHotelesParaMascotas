from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):

        # Enforce that child classes must define these attributes

        if not hasattr(self, "fields_required_for_post"):
            raise AttributeError(
                f"{self.__class__.__name__} must define 'fields_required_for_post'."
                " They are all the fields that must be included with a POST."
            )
        if not hasattr(self, "fields_editable"):
            raise AttributeError(
                f"{self.__class__.__name__} must define 'fields_editable'."
                " They are the fields that can be edited with a PUT (all required) or a PATCH (none required)."
            )
        if not hasattr(self, "fields_not_readable"):
            raise AttributeError(
                f"{self.__class__.__name__} must define 'fields_not_readable'."
                " They are the fields that WILL NOT be sent as response for read operations, like full GETs, POST, PUT or PATCH."
            )

        if kwargs.get("context", None) is None:
            kwargs["context"] = {}
        context = kwargs["context"]
        request = context.get("request", None)
        request_method = request.method if request else None

        super().__init__(*args, **kwargs)

        # Initialize all fields as not required
        self._set_required_status_of_fields(self.fields, False)

        if request_method == "POST":
            # For inputs from POST, require certain fields and allow only those
            self._set_required_status_of_fields(self.fields_required_for_post, True)
            self._retain_only_fields(self.fields_required_for_post)

        elif request_method == "PUT":
            # For inputs from PUT, require all editable fields and allow only those
            self._set_required_status_of_fields(self.fields_editable, True)
            self.fields["id"].required = True
            self._retain_only_fields(self.fields_editable)

        elif request_method == "PATCH":
            # For inputs from PATCH, don't require any field and allow only editable fields
            self.fields["id"].required = True
            self._retain_only_fields(self.fields_editable)

        else:
            # For outputs for GET and others, allow only readable fields
            self._remove_fields(self.fields_not_readable)

    # Helper methods ---------------------------------------------------------

    def _set_required_status_of_fields(self, fields: list, required: bool):
        for field_name in fields:
            if self.fields.get(field_name):
                self.fields[field_name].required = required

    def _retain_only_fields(self, allowed_fields: list):
        all_fields = list(self.fields.keys())
        for field_name in all_fields:
            if field_name not in allowed_fields:
                self.fields.pop(field_name, None)

    def _remove_fields(self, not_allowed_fields: list):
        for field_name in not_allowed_fields:
            self.fields.pop(field_name, None)
