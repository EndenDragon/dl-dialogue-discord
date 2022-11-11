class Menu:
    def __init__(self, title=None, **kwargs):
        self.title = title
        self.type = kwargs.get("type", "embed") # embed or modal
        self.previous_menu_id = kwargs.get("previous_menu", None)

        # one or the other
        self.active_data = kwargs.get("active_data", [])
        self.next_menu_ids = kwargs.get("next_menus", [])
