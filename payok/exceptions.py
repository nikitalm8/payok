class PayOKError(Exception):
    """
    Base PayOK Exception
    """
    
    def __init__(self, code: str, message: str):

        self.code = code
        self.message = message

        super().__init__(
            '[%s] PayOK Error: %s' % (code, message),
        )
