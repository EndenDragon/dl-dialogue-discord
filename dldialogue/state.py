from .data_type import SingleOption, OptionType, StringType, BooleanType, FloatType
from flask_discord_interactions import Message, TextStyles, ActionRow, Button, ButtonStyles, ComponentType, Modal, TextInput, InteractionType, Embed
from .menu_mapping import menu_mapping
from .image_cache_item import ImageCacheItem
import urllib.parse
import requests
import io

class State:
    URL_PROPS = ["type", "name", "text"]
    PARAMS = [
        "nobg", "bg", "bgx", "bgy", "bgr", "bgs", "bgo", "bgflipx", "noportrait",
        "id", "pt", "x", "y", "r", "s", "o", "flipx", "f", "e", "es", "ex", "ey",
    ]

    def __init__(self, ctx, state_id, image_cache, dia_type="dialogue"):
        self.state_id = state_id
        self.current_menu = "home"
        self.ctx = ctx
        self.image_cache = image_cache

        self.type = OptionType(
            "type",
            "Dialogue Kind",
            default = SingleOption(dia_type),
            options = [
                SingleOption("dialogue"),
                SingleOption("intro"),
                SingleOption("caption"),
                SingleOption("full", "Fullscreen"),
                SingleOption("narration"),
                SingleOption("book")
            ]
        )

        self.name = StringType(
            "name",
            "Speaker Name",
            required = True
        )
        self.text = StringType(
            "text",
            "Speaker Speech",
            text_style = TextStyles.PARAGRAPH,
            required = True
        )
        self.f = OptionType(
            "f",
            "Text Font",
            default = SingleOption("en", "English"),
            options = [
                SingleOption("en", "English"),
                SingleOption("ja", "Japanese"),
                SingleOption("zh_tw", "Chinese (Traditional)"),
                SingleOption("zh_cn", "Chinese (Simplified)")
            ]
        )
        
        self.nobg = BooleanType("nobg", "Exclude Background Image")
        self.bg = StringType("bg", "Background Image URL")
        self.bgx = FloatType(
            "bgx",
            "X-Offset",
            min = -400,
            max = 400
        )
        self.bgy = FloatType(
            "bgy",
            "Y-Offset",
            min = -400,
            max = 400
        )
        self.bgr = FloatType(
            "bgr",
            "Rotation",
            min = -180,
            max = 180,
            increment = 0.1
        )
        self.bgs = FloatType(
            "bgs",
            "Scale",
            default = 1,
            min = 0,
            max = 3,
            increment = 0.1
        )
        self.bgo = FloatType(
            "bgo",
            "Opacity",
            default = 1,
            min = 0,
            max = 1,
            increment = 0.01
        )
        self.bgflipx = BooleanType("bgflipx", "Flip Background")

        self.noportrait = BooleanType("noportrait", "Exclude Portrait")
        self.id = StringType("id", "Character ID")
        self.pt = StringType(
            "pt",
            "Portrait Image URL",
        )
        self.x = FloatType(
            "x",
            "X-Offset",
            min = -400,
            max = 400
        )
        self.y = FloatType(
            "y",
            "Y-Offset",
            min = -400,
            max = 400
        )
        self.r = FloatType(
            "r",
            "Rotation",
            min = -180,
            max = 180,
            increment = 0.1
        )
        self.s = FloatType(
            "s",
            "Scale",
            default = 1,
            min = 0,
            max = 3,
            increment = 0.1
        )
        self.o = FloatType(
            "o",
            "Opacity",
            default = 1,
            min = 0,
            max = 1,
            increment = 0.01
        )
        self.flipx = BooleanType("flipx", "Flip Portrait")

        self.e = OptionType(
            "e",
            "Type",
            default = SingleOption("none"),
            options = [
                SingleOption("none"),
                SingleOption("anger"),
                SingleOption("bad"),
                SingleOption("exclamation"),
                SingleOption("heart"),
                SingleOption("inspiration"),
                SingleOption("note"),
                SingleOption("notice"),
                SingleOption("question"),
                SingleOption("sleep"),
                SingleOption("sweat")
            ]
        )
        self.es = OptionType(
            "es",
            "Direction",
            default = SingleOption("l", "Left"),
            options = [
                SingleOption("l", "Left"),
                SingleOption("r", "Right")
            ]
        )
        self.ex = FloatType(
            "ex",
            "X-Offset",
            min = -200,
            max = 200
        )
        self.ey = FloatType(
            "ey",
            "Y-Offset",
            min = -200,
            max = 200
        )

    def make_menu_button(self, state_args, menu_id, label=None, style=ButtonStyles.PRIMARY):
        menu_name = label
        if not label:
            menu_name = menu_mapping[menu_id].title
            if not menu_name and menu_id.startswith("data_"):
                menu_name = getattr(self, menu_id[len("data_"):]).description
        return Button(
            style=style,
            custom_id=state_args + ["navmenu/" + menu_id],
            label=menu_name,
        )

    def data_execute(self, ctx, data_id, state_args, action):
        return getattr(self, data_id).execute(ctx, state_args, action)

    def make_response(self, ctx, handle_state_func, action, update=True):
        state_args = [handle_state_func, self.state_id]
        modal = None
        if action and action.startswith("navmenu/"):
            self.current_menu = action[len("navmenu/"):]
        elif self.current_menu.startswith("data_"):
            modal = self.data_execute(ctx, self.current_menu[len("data_"):], state_args, action)
        if ctx.type == InteractionType.MODAL_SUBMIT:
            prev_menu = menu_mapping[self.current_menu].previous_menu_id
            if prev_menu:
                self.current_menu = prev_menu
        menu_msg, menu_modal = self.get_discord_repr_menu(state_args, update)
        if modal is not None:
            menu_modal = modal
        return (menu_msg, menu_modal)

    def url_encode(self, string):
        if not string:
            return ""
        return urllib.parse.quote(string, safe="")

    def get_embed(self):
        menu_title = menu_mapping[self.current_menu].title
        if not menu_title and self.current_menu.startswith("data_"):
            menu_title = getattr(self, self.current_menu[len("data_"):]).description
        image_url = f"http://api.dldialogue.xyz/{self.type.value.value}/{self.url_encode(self.name.value)}/{self.url_encode(self.text.value)}"
        query = {}
        for param in State.PARAMS:
            val = getattr(self, param)
            if val.value is None or val.value == False:
                continue
            query[param] = str(val)
        image_url = image_url + "?" + urllib.parse.urlencode(query)
        file_obj = self.get_image_file_object(image_url)
        file_return = None
        if file_obj is not None:
            image_url = "attachment://dialogue.png"
            file_return = ("dialogue.png", file_obj, "image/png")
        return (Embed(
            title = f"Dragalia Lost Dialogue Screen Generator ({self.type.value.name})",
            description = "Powered by dldialogue.xyz",
            url = "https://discord.com/oauth2/authorize?client_id=1040955921792245781&scope=bot",
            color = 2728830,
            image = {"url": image_url},
            footer = {"text": menu_title}
        ), file_return)

    def get_image_file_object(self, url):
        for cache in self.image_cache:
            if cache.url == url:
                return cache.get_file_object()
        print(url)
        response = requests.get(url)
        if response.status_code < 200 or response.status_code >= 300 or response.headers.get("Content-Type", None) != "image/png":
            return None
        file_obj = io.BytesIO(response.content)
        file_obj.seek(0)
        self.image_cache.append(ImageCacheItem(url, file_obj))
        return file_obj

    def get_discord_repr_menu(self, state_args, update):
        current_menu = menu_mapping[self.current_menu]
        components = []
        if current_menu.next_menu_ids:
            for menu_id in current_menu.next_menu_ids:
                components.append(self.make_menu_button(state_args, menu_id))
        if current_menu.active_data:
            for data_id in current_menu.active_data:
                components.append(getattr(self, data_id).get_discord_repr(state_args))
        rows = self.split_action_rows(components)
        modal = None
        if current_menu.type == "modal":
            modal = Modal(
                state_args + [self.current_menu],
                current_menu.title,
                rows
            )
            rows = []
        if current_menu.previous_menu_id:
            rows = rows + [ActionRow(components=[self.make_menu_button(state_args, current_menu.previous_menu_id, "Back", ButtonStyles.SECONDARY)])]
        embed, file_response = self.get_embed()
        return (Message(
            embed = embed,
            components = rows,
            update = update,
            file = file_response
        ), modal)

    def split_action_rows(self, components):
        rows = []
        count = 0
        for component in components:
            if component.type == ComponentType.ACTION_ROW:
                rows.append(component)
                count = 0
                continue
            if count % 5 == 0:
                rows.append(ActionRow(components=[]))
            rows[-1].components.append(component)
            count = count + 1
        return rows

