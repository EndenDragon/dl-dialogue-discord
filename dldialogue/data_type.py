from flask_discord_interactions import TextStyles, SelectMenuOption, SelectMenu, TextInput, ActionRow, Button, ButtonStyles, Modal
from flask import abort

class SingleOption:
    def __init__(self, value, name=None):
        self.value = value
        if name:
            self.name = name
        else:
            self.name = value.capitalize()

    def __str__(self):
        return self.value

    def get_discord_repr(self, state_args):
        return SelectMenuOption(
            label = self.name,
            value = self.value
        )

class OptionType:
    def __init__(self, id, description, **kwargs):
        self.id = id
        self.description = description
        self.default = kwargs.get("default", None)
        self.options = kwargs.get("options", [])
        self.value = self.default

    def __str__(self):
        if self.value is None:
            return ""
        return self.value.value

    def set_from_string(self, value):
        if value is "":
            self.value = self.default
            return
        for option in self.options:
            if option.value == value:
                self.value = option
                break

    def get_discord_repr(self, state_args):
        options = []
        for option in self.options:
            rep = option.get_discord_repr(state_args)
            rep.default = self.default and self.default.value == option.value
            options.append(rep)
        return SelectMenu(
            placeholder = self.description,
            custom_id = state_args + [self.value],
            max_values = 1,
            options = options
        )

    def execute(self, ctx, state_args, action):
        value = ctx.values[0]
        for option in self.options:
            if option.value == value:
                self.value = option
                self.default = self.value
                break
        return None

class StringType:
    def __init__(self, id, description, **kwargs):
        self.id = id
        self.description = description
        self.default = kwargs.get("default", None)
        self.text_style = kwargs.get("text_style", TextStyles.SHORT)
        self.required = kwargs.get("required", False)
        self.value = self.default
    
    def __str__(self):
        if self.value is None:
            return ""
        return self.value

    def set_from_string(self, value):
        if value == "":
            self.value = None
        else:
            self.value = value

    def get_discord_repr(self, state_args):
        return ActionRow(
            components = [
                TextInput(
                    label = self.description,
                    custom_id = state_args + [self.id],
                    style = self.text_style,
                    value = self.value,
                    placeholder = self.description,
                    required = self.required,
                    max_length = 300,
                )
            ]
        )
    
    def execute(self, ctx, state_args, action):
        value = ctx.components[0].components[0].value
        self.value = value
        return None

class BooleanType:
    def __init__(self, id, description, **kwargs):
        self.id = id
        self.description = description
        self.default = kwargs.get("default", False)
        self.value = self.default
    
    def __str__(self):
        return str(self.value)

    def set_from_string(self, value):
        self.value = value == "True"

    def get_discord_repr(self, state_args):
        return ActionRow(
            components = [
                Button(
                    style = ButtonStyles.SUCCESS,
                    custom_id = state_args + [True],
                    label = "Yes"
                ),
                Button(
                    style = ButtonStyles.DANGER,
                    custom_id = state_args + [False],
                    label = "No"
                )
            ]
        )

    def execute(self, ctx, state_args, action):
        self.value = action == "True"
        return None

class FloatType:
    def __init__(self, id, description, **kwargs):
        self.id = id
        self.description = description
        self.default = kwargs.get("default", 0)
        self.min = kwargs.get("min", -10)
        self.max = kwargs.get("max", 10)
        self.increment = kwargs.get("increment", 1)
        self.value = self.default

    def __str__(self):
        return str(self.value)

    def set_from_string(self, value):
        self.value = float(value)

    def get_discord_repr(self, state_args):
        increment_lowest = -1 * 10 * self.increment
        increment_low = -1 * self.increment
        increment_high = self.increment
        increment_highest = 10 * self.increment
        return ActionRow(
            components = [
                Button(
                    style = ButtonStyles.DANGER,
                    custom_id = state_args + [f"add/{increment_lowest}"],
                    label = str(increment_lowest)
                ),
                Button(
                    style = ButtonStyles.DANGER,
                    custom_id = state_args + [f"add/{increment_low}"],
                    label = str(increment_low)
                ),
                Button(
                    style = ButtonStyles.PRIMARY,
                    custom_id = state_args + ["launch_modal"],
                    label = str(self.value)
                ),
                Button(
                    style = ButtonStyles.SUCCESS,
                    custom_id = state_args + [f"add/{increment_high}"],
                    label = "+" + str(increment_high)
                ),
                Button(
                    style = ButtonStyles.SUCCESS,
                    custom_id = state_args + [f"add/{increment_highest}"],
                    label = "+" + str(increment_highest)
                ),
            ]
        )

    def execute(self, ctx, state_args, action):
        if action.startswith("add/"):
            self.set_value(self.value + float(action[len("add/"):]))
        elif action == "set":
            value = ctx.components[0].components[0].value
            try:
                self.set_value(float(value))
            except ValueError:
                abort(400)
        elif action == "launch_modal":
            return Modal(
                state_args + [f"set"],
                self.description,
                [
                    ActionRow(
                        [
                            TextInput(
                                label = self.description + f" ({self.min} - {self.max})",
                                custom_id = state_args + [f"set_value"],
                                style = TextStyles.SHORT,
                                value = str(self.value),
                                placeholder = self.description,
                                required = False,
                                max_length = 8,
                            )
                        ]
                    )
                ],
            )
        return None

    def set_value(self, new_value):
        self.value = min(max(self.min, new_value), self.max)
