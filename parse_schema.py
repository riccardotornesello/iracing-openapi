import json

results = json.load(open("results.json"))

schema = []

type_whitelist = {
    # "wheel_color": "string",
    # "session_start_time": "int",
}


def extract_schema(data):
    for k, v in data.items():
        camel_name = "".join([w.capitalize() for w in k.split("_")])

        t = None
        if k in type_whitelist:
            t = type_whitelist[k]
        elif type(v) == int:
            t = "int"
        elif type(v) == str:
            t = "string"
        elif type(v) == float:
            t = "float32"
        elif type(v) == bool:
            t = "bool"
        elif type(v) == list:
            if not v:
                raise Exception(f"Empty list for {k}")
                continue
            elif type(v[0]) == int:
                t = "[]int"
            elif type(v[0]) == str:
                t = "[]string"
            elif type(v[0]) == float:
                t = "[]float32"
            elif type(v[0]) == bool:
                t = "[]bool"
            elif type(v[0]) == dict:
                schema.append(f"{camel_name} []struct {{")
                extract_schema(v[0])
                schema.append(f'}} `json:"{k}"`')
            else:
                raise Exception(f"Unknown type for {k}: {v}")
        elif type(v) == dict:
            schema.append(f"{camel_name} struct {{")
            extract_schema(v)
            schema.append(f'}} `json:"{k}"`')
        else:
            raise Exception(f"Unknown type for {k}: {v}")

        if t:
            schema.append(f'{camel_name} {t} `json:"{k}"`')


extract_schema(results)
print("\n".join(schema))
