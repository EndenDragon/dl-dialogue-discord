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
import threading
import time

from requests import HTTPError

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

def make_state(ctx, dia_type):
    state_id = str(uuid.uuid4())
    new_state = State(ctx, state_id, dia_type)
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
    print("honk1", ctx.token, ctx.followup_url())
    current_state = get_state(state_id)
    print(action, update, current_state.current_menu)
    response, modal = current_state.make_response(ctx, handle_state, action, update)
    if update:
        try:
            current_state.ctx.edit(response)
        except HTTPError as e:
            print(e.response.text)
            print(e.request.body)
    if modal is None:
        return response
    # modal = Modal(
    #     "honkhonk",
    #     "Tell me about yourself",
    #     [
    #         ActionRow(
    #             [
    #                 TextInput(
    #                     custom_id="name",
    #                     label="What's your name?",
    #                     placeholder="John Doe",
    #                     style=TextStyles.SHORT,
    #                     required=True,
    #                 )
    #             ]
    #         )
    #     ],
    # )
    print(modal.encode())
    return modal

@discord.command(name="dialogue", description="Creates a Dragalia dialogue")
def command_dialogue(ctx):
    da_state = make_state(ctx.freeze(), "dialogue")
    return handle_state_prime(ctx, da_state.state_id, None)

discord.set_route("/discord")