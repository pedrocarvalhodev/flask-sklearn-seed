from schema import Schema, And, Use


def validate(schema_name, json_data):
    if schema_name == 'predict':
        schema = _predict_schema()
    else:
        raise NotImplementedError("Schema name: '{}' not found.".format(schema_name))

    # let exceptions bubble up
    schema.validate(json_data)


def _predict_schema():
    schema = Schema(
        {
            'id': And(Use(str)),
            'x_1': And(Use(float)),
            'x_2': And(Use(float)),
            'x_3': And(Use(float)),
            'x_4': And(Use(float))
        })

    return schema
