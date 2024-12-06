import re

from pydantic import BaseModel, ValidationInfo, field_validator


class FormInput(BaseModel):
    form: str

    @field_validator("form")
    @classmethod
    def form_validator(cls, v: str, info: ValidationInfo):
        form = re.fullmatch(
            r"^(([^=]+=[^=]+)(&[^=]+=[^=]+)?)+$", v
        )
        assert form is not None, f"{info.field_name} is not valid"
        return form.string
