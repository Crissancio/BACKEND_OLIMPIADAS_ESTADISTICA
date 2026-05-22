class CSVImportError(Exception):

    def __init__(
        self,
        message: str
    ):

        self.message = message

        super().__init__(message)

class MissingColumnsError(CSVImportError):
    pass

class InvalidCodigoError(CSVImportError):
    pass

class DuplicateCodigoError(CSVImportError):
    pass

class InvalidNombreError(CSVImportError):
    pass

class InvalidDependenciaError(CSVImportError):
    pass

class InvalidTurnoError(CSVImportError):
    pass

class InvalidTelefonoError(CSVImportError):
    pass

class InvalidDirectorError(CSVImportError):
    pass