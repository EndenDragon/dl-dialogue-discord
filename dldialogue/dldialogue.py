from config import config
from .state import State
from flask import Flask
from collections import deque
from flask_discord_interactions import (
    DiscordInteractions,
    Message,
    Modal,
    TextInput,
    TextStyles,
    ActionRow,
    Button,
)
import uuid

app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = config["DISCORD_CLIENT_ID"]
app.config["DISCORD_PUBLIC_KEY"] = config["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = config["DISCORD_CLIENT_SECRET"]

state_storage = deque(maxlen=50)

def get_state(state_id):
    for single_state in state_storage:
        if single_state.state_id == state_id:
            return single_state
    return None

def make_state(dia_type):
    state_id = str(uuid.uuid4())
    new_state = State(state_id, dia_type)
    state_storage.append(new_state)
    return new_state

@discord.command(name="ping", description="Pings the server")
def command_ping(ctx):
    return Message(
        content="Pong!"
    )

@discord.custom_handler()
def handle_state(ctx, state_id, action):
    return handle_state_prime(ctx, state_id, action, True)

def handle_state_prime(ctx, state_id, action, update=False):
    current_state = get_state(state_id)
    print(action, update, current_state.current_menu)
    response = current_state.make_response(handle_state, action, update)
    # if update:
    #     ctx.edit(response)
    return response

@discord.command(name="dialogue", description="Creates a Dragalia dialogue")
def command_dialogue(ctx):
    da_state = make_state("dialogue")
    return handle_state_prime(None, da_state.state_id, None)

discord.set_route("/discord")
