import os
import uuid

from .utils import get_resized_image


class GetUploadToMixin(object):
    dynamic_image_fields = None

    def get_upload_to(self, field_name=None):
        prefix = "{}/{}".format(
            self._meta.app_label.lower(), self._meta.model_name.lower()
        )

        def upload_to(instance, file_name):
            if self.dynamic_image_fields is not None:
                if field_name in self.dynamic_image_fields.keys():
                    name = uuid.uuid4().hex
                    ext = file_name.split(".")[-1]
                    file_name = "{}.{}".format(name, ext)
            return os.path.normpath("{}/{}".format(prefix, file_name))

        return upload_to


class ResizeImageFieldsMixin(object):
    dynamic_image_fields = None

    def resize_image_field(self, source_field, dest_field_name, dimensions):
        dest_field = getattr(self, dest_field_name, None)
        if all([x is not None for x in (source_field, dest_field)]):
            name = source_field.name.split("/")[-1].split(".")[0]
            if not dest_field or name not in dest_field.name:
                setattr(
                    self,
                    dest_field_name,
                    get_resized_image(
                        source_field, image_format="jpeg", dimensions=dimensions
                    ),
                )
                self.save()

    def resize_image_fields(self):
        if self.dynamic_image_fields is not None:
            for s_field_name, s_field_data in self.dynamic_image_fields.items():
                s_field = getattr(self, s_field_name, None)
                if s_field:
                    resize = s_field_data.get("resize", None)
                    if resize is not None:
                        for d_field_name, d_field_data in resize.items():
                            d_field_dims = d_field_data["dimensions"]
                            self.resize_image_field(s_field, d_field_name, d_field_dims)


class ClearImageFieldsMixin(object):
    dynamic_image_fields = None

    def clear_image_field(self, field_name):
        field = getattr(self, field_name, None)
        if field is not None:
            field.delete()

    def clear_image_fields(self):
        if self.dynamic_image_fields is not None:
            for s_field_name, s_field_data in self.dynamic_image_fields.items():
                s_field = getattr(self, s_field_name, None)
                if not s_field:
                    clear = s_field_data.get("clear", None)
                    if clear is not None:
                        for d_field_name in clear:
                            self.clear_image_field(d_field_name)
