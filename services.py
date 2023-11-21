async def find_matching_template(document: dict, typed_data: dict) -> str:
    template_fields = list(document.keys())
    name_form = document["name"]
    template_fields.remove("name")
    template_fields.remove("_id")
    if all(field in typed_data and document.get(field) == typed_data.get(field) for field in template_fields):
        return name_form
