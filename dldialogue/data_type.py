from flask_discord_interactions import TextStyles, SelectMenuOption, SelectMenu, TextInput, ActionRow, Button, ButtonStyles

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
    def __init__(self, description, **kwargs):
        self.description = description
        self.default = kwargs.get("default", None)
        self.options = kwargs.get("options", [])
        self.value = self.default

    def __str__(self):
        return self.value

    def get_discord_repr(self, state_args):
        options = []
        for option in self.options:
            rep = option.get_discord_repr(state_args)
            rep.default = self.default and self.default.value == option.value
            options.append(rep)
        return SelectMenu(
            placeholder = self.description,
            custom_id = state_args + [value],
            max_values = 1,
            options = options
        )

class StringType:
    def __init__(self, description, **kwargs):
        self.description = description
        self.default = kwargs.get("default", None)
        self.text_style = kwargs.get("text_style", TextStyles.SHORT)
        self.value = self.default
    
    def __str__(self):
        return self.value

    def get_discord_repr(self, state_args):
        return TextInput(
            label = self.description,
            custom_id = state_args + [value],
            style = self.text_style,
            value = self.value
        )

class BooleanType:
    def __init__(self, description, **kwargs):
        self.description = description
        self.default = kwargs.get("default", False)
        self.value = self.default
    
    def __str__(self):
        return self.value

    def get_discord_repr(self, state_args):
        return ActionRow(
            components = [
                Button(
                    style = ButtonStyles.PRIMARY,
                    custom_id = state_args + [True],
                    label = "Yes"
                ),
                Button(
                    style = ButtonStyles.PRIMARY,
                    custom_id = state_args + [False],
                    label = "No"
                )
            ]
        )

class FloatType:
    def __init__(self, description, **kwargs):
        self.description = description
        self.default = kwargs.get("default", 0)
        self.min = kwargs.get("min", -10)
        self.max = kwargs.get("max", 10)
        self.increment = kwargs.get("increment", 1)
        self.value = self.default

    def __str__(self):
        return self.value

    def get_discord_repr(self, state_args):
        return TextInput(
            label = self.description,
            custom_id = state_args + [value],
            style = TextStyles.SHORT,
            value = self.value
        )
