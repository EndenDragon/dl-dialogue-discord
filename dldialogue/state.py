from data_type import SingleOption, OptionType, StringType, BooleanType, FloatType

class State:
    type = OptionType(
        default = SingleOption("dialogue"),
        options = [
            SingleOption("intro"),
            SingleOption("caption"),
            SingleOption("full", "Fullscreen"),
            SingleOption("narration"),
            SingleOption("book")
        ]
    )
    name = StringType()
    text = StringType()
    
    nobg = BooleanType()
    bg = StringType()
    bgx = FloatType(
        min = -400,
        max = 400
    )
    bgy = FloatType(
        min = -400,
        max = 400
    )
    bgs = FloatType(
        default = 1
        min = 0,
        max = 3,
        increment = 0.1
    )
    bgo = FloatType(
        default = 1
        min = 0,
        max = 1,
        increment = 0.01
    )
    bgflipx = BooleanType()
    noportrait = BooleanType()
    id = StringType()
    pt = StringType()
    x = FloatType(
        min = -400,
        max = 400
    )
    y = FloatType(
        min = -400,
        max = 400
    )
    r = FloatType(
        min = -180,
        max = 180,
        increment = 0.1
    )
    s = FloatType(
        default = 1,
        min = 0,
        max = 3,
        increment = 0.1
    )
    o = FloatType(
        default = 1,
        min = 0,
        max = 1,
        increment = 0.01
    )
    flipx = BooleanType()
    f = OptionType(
        default = SingleOption("en", "English"),
        options = [
            SingleOption("en", "English"),
            SingleOption("ja", "Japanese"),
            SingleOption("zh_tw", "Chinese (Traditional)"),
            SingleOption("zh_cn", "Chinese (Simplified)")
        ]
    )
    e = OptionType(
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
    es = OptionType(
        default = SingleOption("l", "Left"),
        options = [
            SingleOption("l", "Left"),
            SingleOption("r", "Right")
        ]
    )
    ex = FloatType(
        min = -200,
        max = 200
    )
    ey = FloatType(
        min = -200,
        max = 200
    )
