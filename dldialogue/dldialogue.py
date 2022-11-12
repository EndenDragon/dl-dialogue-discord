from config import config
from .state import State
from flask import Flask
from collections import deque
from .data_type import SingleOption
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

@discord.command(name="ping", description="Send a ping")
def command_ping(ctx):
    return handle_command(ctx, "dialogue", {
        "name": "Althemia?",
        "text": "Pong!",
        "pt": "https://dragalialost.wiki/images/0/06/110047_02_base_portrait.png",
        "bg": "https://dragalialost.wiki/images/6/67/Sty_bg_0005_102_00.png",
        "s": 3,
        "y": -70,
        "r": 20,
        "e": SingleOption("exclamation"),
        "ey": 130,
        "f": SingleOption("ja", "Japanese"),
    })

@discord.custom_handler()
def handle_state(ctx, state_id, action):
    return handle_state_prime(ctx, state_id, action, True)

def handle_state_prime(ctx, state_id, action, update=False):
    print("honk1", ctx.token, ctx.followup_url())
    current_state = get_state(state_id)
    if ctx.author.id != current_state.ctx.author.id:
        return Message(content=f"This is not your dialogue, <@{ctx.author.id}>!", ephemeral=True)
    print(action, update, current_state.current_menu)
    response, modal = current_state.make_response(ctx, handle_state, action, update)
    if update:
        try:
            current_state.ctx.edit(response)
        except HTTPError as e:
            print(e.response.text)
            print(e.request.body)
    print("modaler", modal)
    if modal is None:
        return response
    print(modal.encode())
    return modal

def handle_command(ctx, dia_type, defaults=None):
    da_state = make_state(ctx.freeze(), dia_type)
    if defaults:
        for key, val in defaults.items():
            getattr(da_state, key).value = val
    return handle_state_prime(ctx, da_state.state_id, None)

@discord.command(name="dialogue", description="Creates a Dragalia dialogue!")
def command_dialogue(ctx):
    return handle_command(ctx, "dialogue", {
        "name": "Sarisse",
        "text": "With a bang, I'm on the scene!",
        "pt": "https://dragalialost.wiki/images/3/33/100029_04_base_portrait.png",
        "bg": "https://dragalialost.wiki/images/3/30/Sty_bg_0021_100_00.png",
    })

@discord.command(name="introduction", description="Creates a Dragalia introduction dialogue!")
def command_introduction(ctx):
    return handle_command(ctx, "intro", {
        "name": "Botan",
        "text": "Naginata Cutie",
        "pt": "https://dragalialost.wiki/images/0/00/110312_01_base_portrait.png",
        "nobg": True,
        "s": 1.5,
    })

@discord.command(name="caption", description="Creates a Dragalia caption dialogue!")
def command_caption(ctx):
    return handle_command(ctx, "caption", {
        "name": "Mitsuba's Kitchen",
        "text": "2 days before the Gala Festival",
        "pt": "https://dragalialost.wiki/images/a/a5/110027_04_base_portrait.png",
        "bg": "https://dragalialost.wiki/images/a/a3/Sty_bg_0031_100_00.png",
    })

@discord.command(name="fullscreen", description="Creates a Dragalia fullscreen dialogue!")
def command_fullscreen(ctx):
    return handle_command(ctx, "full", {
        "name": "Fleur",
        "text": "i am artist",
        "pt": "https://dragalialost.wiki/images/e/e1/110319_01_base_portrait.png",
    })

@discord.command(name="narration", description="Creates a Dragalia narration dialogue!")
def command_narration(ctx):
    return handle_command(ctx, "narration", {
        "name": "Alex",
        "text": "Beach security mission is a go.",
        "pt": "https://dragalialost.wiki/images/7/78/100005_08_base_portrait.png",
        "bg": "https://dragalialost.wiki/images/d/d2/Sty_bg_0037_100_00.png",
    })

@discord.command(name="book", description="Creates a Dragalia book dialogue!")
def command_book(ctx):
    return handle_command(ctx, "book", {
        "name": "Mym",
        "text": "Behold, the power of the Flamewyrm!",
        "noportrait": True,
        "nobg": True,
    })

discord.set_route("/discord")