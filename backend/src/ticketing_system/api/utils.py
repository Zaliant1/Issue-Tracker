from bson import ObjectId


def json_ready(data):
    if isinstance(data, ObjectId):
        return str(data)
    else:
        return data


def prepare_json(data):
    if isinstance(data, dict):
        output = {}
        for key, value in data.items():
            if isinstance(value, dict) or isinstance(value, list):
                output[key] = prepare_json(value)
            else:
                output[key] = json_ready(value)

        return output

    elif isinstance(data, list):
        output = []
        for value in data:
            if isinstance(value, dict) or isinstance(value, list):
                output.append(prepare_json(value))
            else:
                output[key] = json_ready(value)

        return output
    else:
        return json_ready(data)
