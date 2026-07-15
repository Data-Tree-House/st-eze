class GFinanceError(Exception):
    def __init__(
        self,
        message: str,
        sheet_id: str | None = None,
    ):
        self.sheet_id: str | None = sheet_id
        super().__init__(message)
