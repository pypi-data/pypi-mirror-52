class AbstractBaseController:
    pass


class MetaController(AbstractBaseController):
    required_controller = []

    def __init__(self):
        super().__init__()


class SerialController(AbstractBaseController):
    required_boards = []

    def __init__(self):
        super().__init__()
