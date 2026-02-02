from marshmallow import Schema, fields, validate

class PSPSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    contract = fields.Str(allow_none=True)
    vision = fields.Str(allow_none=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    status = fields.Str()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    psp_id = fields.Int(required=True)
    description = fields.Str(allow_none=True)
    category = fields.Str(required=True)
    start_date = fields.Date(required=True)
    due_date = fields.Date(allow_none=True)
    completed_value = fields.Float()
    target_value = fields.Float()
    unit = fields.Str(allow_none=True)
    completed = fields.Bool()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
