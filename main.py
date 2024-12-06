import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from pydantic import ValidationError

from settings import settings
from schemas import FormInput
from validators import get_validator, get_field_type
from db import get_schemas


app = FastAPI(
    title=settings.app_name,
)


@app.post("/get_form", tags=["Form"], name="Получение формы")
async def get_form(request: Request):
    try:
        form = FormInput(form=(await request.body()).decode())
    except ValidationError:
        raise HTTPException(422, "Form is not valid")
    form_schemas = get_schemas()
    fields = {}
    for pair in form.form.strip("&").split("&"):
        try:
            name, value = pair.split("=")
        except ValueError:
            raise HTTPException(422, "Form is not valid")
        fields[name] = value
    existed_schema = {"priority": 0, "count": 0, "name": None}
    form_keys = set(fields.keys())
    for schema in form_schemas:
        schema_keys = set([key for key in schema.keys() if key != "name"])
        intersection = schema_keys.intersection(form_keys)
        if intersection == schema_keys:
            fields_priority = 0
            for field, field_type in schema.items():
                if field == "name":
                    continue
                value = fields[field]
                if field_type == "text":
                    continue
                validator = get_validator(field_type)
                if not get_validator(field_type)(value):
                    break
                fields_priority += validator.get_priority()
            else:
                if existed_schema["count"] <= len(intersection) and existed_schema["priority"] <= fields_priority:
                    existed_schema["count"] = len(intersection)
                    existed_schema["priority"] = fields_priority
                    existed_schema["name"] = schema["name"]

    if not existed_schema["name"]:
        types = {}
        for field, value in fields.items():
            types[field] = get_field_type(value)
        return types
    return existed_schema.get("name", "unnamed")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
