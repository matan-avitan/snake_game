from pydantic import BaseModel


class ButtonOption(BaseModel):
    text: str
    color: str
    value: object


class ButtonOptions:

    def __init__(self):
        self.color_buttons = [
            ButtonOption(text='Red', color='red', value='red'),
            ButtonOption(text='Green', color='green', value='green'),
            ButtonOption(text='Brown', color='brown', value='brown')
        ]
        self.board_types = [
            ButtonOption(text='Grass', color='green', value='grass'),
            ButtonOption(text='Stone', color='gray', value='stone'),
            ButtonOption(text='Sand', color='brown', value='sand')
        ]
        self.difficult_types = [
            ButtonOption(text='Easy', color='green', value='easy'),
            ButtonOption(text='Medium', color='orange', value='medium'),
            ButtonOption(text='Hard', color='red', value='hard')
        ]
        self.darkness_mode_options = [
            ButtonOption(text='Off', color='gold', value=False),
            ButtonOption(text='On', color='gold', value=True)
        ]
