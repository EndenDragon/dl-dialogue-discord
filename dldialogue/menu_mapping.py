from .menu import Menu

menu_mapping = {
    "home": Menu(
        "Customize your Dragalia Dialogue",
        type = "embed",
        next_menus = [
            "text_main",
            "background_main",
            "portrait_main",
            "emotion_main"
        ]
    ),

    "text_main": Menu(
        "Text Settings",
        type = "embed",
        next_menus = [
            "data_name",
            "data_text",
            "data_f",
        ],
        previous_menu = "home",
    ),
    "data_name": Menu(
        "Name",
        type = "modal",
        active_data = [
            "name",
        ],
        previous_menu = "text_main",
    ),
    "data_text": Menu(
        "Text",
        type = "modal",
        active_data = [
            "text"
        ],
        previous_menu = "text_main",
    ),
    "data_f": Menu(
        "Font",
        type = "embed",
        active_data = [
            "f"
        ],
        previous_menu = "text_main",
    ),

    "background_main": Menu(
        "Background Settings",
        type = "embed",
        previous_menu = "home",
        next_menus = [
            "data_nobg",
            "data_bg",
            "data_bgx",
            "data_bgy",
            "data_bgr",
            "data_bgs",
            "data_bgo",
            "data_bgflipx"
        ]
    ),
    "data_nobg": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["nobg"]
    ),
    "data_bg": Menu(
        "Background Image URL",
        type = "modal",
        previous_menu = "background_main",
        active_data = ["bg"]
    ),
    "data_bgx": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgx"]
    ),
    "data_bgy": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgy"]
    ),
    "data_bgr": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgr"]
    ),
    "data_bgs": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgs"]
    ),
    "data_bgo": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgo"]
    ),
    "data_bgflipx": Menu(
        type = "embed",
        previous_menu = "background_main",
        active_data = ["bgflipx"]
    ),

    "portrait_main": Menu(
        "Portrait Settings",
        type = "embed",
        previous_menu = "home",
        next_menus = [
            "data_noportrait",
            "data_id",
            "data_pt",
            "data_x",
            "data_y",
            "data_r",
            "data_s",
            "data_o",
            "data_flipx",
        ]
    ),
    "data_noportrait": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["noportrait"]
    ),
    "data_id": Menu(
        "Character ID",
        type = "modal",
        previous_menu = "portrait_main",
        active_data = ["id"]
    ),
    "data_pt": Menu(
        "Portrait Image URL",
        type = "modal",
        previous_menu = "portrait_main",
        active_data = ["pt"]
    ),
    "data_x": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["x"]
    ),
    "data_y": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["y"]
    ),
    "data_r": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["r"]
    ),
    "data_s": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["s"]
    ),
    "data_o": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["o"]
    ),
    "data_flipx": Menu(
        type = "embed",
        previous_menu = "portrait_main",
        active_data = ["flipx"]
    ),

    "emotion_main": Menu(
        "Emotion Settings",
        type = "embed",
        previous_menu = "home",
        next_menus = [
            "data_e",
            "data_es",
            "data_ex",
            "data_ey",
        ]
    ),
    "data_e": Menu(
        type = "embed",
        previous_menu = "emotion_main",
        active_data = ["e"]
    ),
    "data_es": Menu(
        type = "embed",
        previous_menu = "emotion_main",
        active_data = ["es"]
    ),
    "data_ex": Menu(
        type = "embed",
        previous_menu = "emotion_main",
        active_data = ["ex"]
    ),
    "data_ey": Menu(
        type = "embed",
        previous_menu = "emotion_main",
        active_data = ["ey"]
    ),
}