from loguru import logger


class W:
    @logger.catch
    def __init__(self) -> None:
        pass
