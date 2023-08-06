class NoConfigError(Exception):

    def __init__(self):
        self.error_msg = """
            [Error]: could not build site. Missing settings.py file.
            Make sure it's correctly named and that it's located in
            the current directory.
        """
        super().__init__(self.error_msg)

    def __str__(self):
        return repr(self.error_msg)
