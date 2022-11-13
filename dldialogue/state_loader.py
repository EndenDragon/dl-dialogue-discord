from .state import State
import json
import tempfile
import os
import types
from flask_discord_interactions import Context

def get_path(state_id):
    return tempfile.gettempdir() + f"/dldia_{state_id}.json"

def get_state(state_id):
    path = get_path(state_id)
    if not os.path.isfile(path):
        return None
    contents = None
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
    contents = json.loads(contents)

    # ctx
    app = types.SimpleNamespace()
    app.config = contents["ctx"]["config"]
    ctx = Context.from_data(app=app, data=contents["ctx"]["data"])
    ctx.frozen_auth_headers = contents["ctx"]["auth_headers"]

    # state
    state = State(ctx, contents["state_id"])
    state.current_menu = contents["state"]["current_menu"]
    for key, val in contents["state"]["props"].items():
        getattr(state, key).set_from_string(val)
    return state

def save_state(app, state):
    state_id = state.state_id
    ctx = state.ctx

    # ctx
    auth_headers = ctx.auth_headers
    CONFIG_KEYS = [
        "DISCORD_BASE_URL",
        "DISCORD_CLIENT_ID",
        "DONT_REGISTER_WITH_DISCORD",
    ]
    config = {key: app.config[key] for key in CONFIG_KEYS}
    data = ctx.data
    if "message" in data:
        data["message"]["embeds"] = []

    # state
    state_props = {}
    for prop in State.URL_PROPS:
        state_props[prop] = str(getattr(state, prop))
    for prop in State.PARAMS:
        state_props[prop] = str(getattr(state, prop))
    current_menu = state.current_menu

    frozen_result = {
        "state_id": state_id,
        "ctx": {
            "auth_headers": auth_headers,
            "config": config,
            "data": data
        },
        "state": {
            "props": state_props,
            "current_menu": current_menu
        }
    }
    with open(get_path(state_id), "w", encoding="utf-8") as f:
        f.write(json.dumps(frozen_result))
