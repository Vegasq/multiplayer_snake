import json


def pack(client_uuid, msg_id):
    return bytes(json.dumps({
        "uuid": client_uuid,
        "message": msg_id
    }), "utf-8")


def unpack(data):
    message = str(data)
    m = json.loads(message)
    return m["uuid"], m["message"]
