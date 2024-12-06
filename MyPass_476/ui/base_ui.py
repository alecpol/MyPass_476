class UIComponent:
    def __init__(self, mediator=None):
        self.mediator = mediator

    def set_mediator(self, mediator):
        self.mediator = mediator
