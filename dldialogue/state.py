from .data_type import SingleOption, OptionType, StringType, BooleanType, FloatType
from flask_discord_interactions import Message, TextStyles, ActionRow, Button, ButtonStyles
from .menu_mapping import menu_mapping

class State:
    def __init__(self, state_id, dia_type="dialogue"):
        self.state_id = state_id
        self.current_menu = "home"

        self.type = OptionType(
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

        self.name = StringType("Speaker Name")
        self.text = StringType(
            "Speaker Speech",
            text_style = TextStyles.PARAGRAPH
        )
        self.f = OptionType(
            "Text Font",
            default = SingleOption("en", "English"),
            options = [
                SingleOption("en", "English"),
                SingleOption("ja", "Japanese"),
                SingleOption("zh_tw", "Chinese (Traditional)"),
                SingleOption("zh_cn", "Chinese (Simplified)")
            ]
        )
        
        self.nobg = BooleanType("Exclude Background Image")
        self.bg = StringType("Background Image URL")
        self.bgx = FloatType(
            "Background X-Offset",
            min = -400,
            max = 400
        )
        self.bgy = FloatType(
            "Background Y-Offset",
            min = -400,
            max = 400
        )
        self.bgr = FloatType(
            "Background Rotation",
            min = -180,
            max = 180,
            increment = 0.1
        )
        self.bgs = FloatType(
            "Background Scale",
            default = 1,
            min = 0,
            max = 3,
            increment = 0.1
        )
        self.bgo = FloatType(
            "Background Opacity",
            default = 1,
            min = 0,
            max = 1,
            increment = 0.01
        )
        self.bgflipx = BooleanType("Flip Background")

        self.noportrait = BooleanType("Exclude Portrait")
        self.id = StringType("Character ID")
        self.pt = StringType("Portrait Image URL")
        self.x = FloatType(
            "Portrait X-Offset",
            min = -400,
            max = 400
        )
        self.y = FloatType(
            "Portrait Y-Offset",
            min = -400,
            max = 400
        )
        self.r = FloatType(
            "Portrait Rotation",
            min = -180,
            max = 180,
            increment = 0.1
        )
        self.s = FloatType(
            "Portrait Scale",
            default = 1,
            min = 0,
            max = 3,
            increment = 0.1
        )
        self.o = FloatType(
            "Portrait Opacity",
            default = 1,
            min = 0,
            max = 1,
            increment = 0.01
        )
        self.flipx = BooleanType("Flip Portrait")

        self.e = OptionType(
            "Emotion Type",
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
            "Emotion Direction",
            default = SingleOption("l", "Left"),
            options = [
                SingleOption("l", "Left"),
                SingleOption("r", "Right")
            ]
        )
        self.ex = FloatType(
            "Emotion X-Offset",
            min = -200,
            max = 200
        )
        self.ey = FloatType(
            "Emotion Y-Offset",
            min = -200,
            max = 200
        )

    def make_menu_button(self, state_args, menu_id):
        menu_name = menu_mapping[menu_id].title
        return Button(
            style=ButtonStyles.PRIMARY,
            custom_id=state_args + ["navmenu/" + menu_id],
            label=menu_name,
        )

    def make_response(self, handle_state_func, action, update=True):
        state_args = [handle_state_func, self.state_id]
        if action and action.startswith("navmenu/"):
            self.current_menu = action[len("navmenu/"):]
        return self.get_discord_repr_menu(state_args, update)

    def get_discord_repr_menu(self, state_args, update):
        current_menu = menu_mapping[self.current_menu]
        buttons = []
        if current_menu.next_menu_ids:
            for menu_id in current_menu.next_menu_ids:
                buttons.append(self.make_menu_button(state_args, menu_id))
        return Message(
            content = "test",
            components = self.split_action_rows(buttons),
            update = update
        )

    def split_action_rows(self, components):
        rows = []
        count = 0
        for component in components:
            if count % 5 == 0:
                rows.append(ActionRow(components=[]))
            rows[-1].components.append(component)
            count = count + 1
        return rows

