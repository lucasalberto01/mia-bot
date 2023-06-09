from unicodedata import normalize


class Clear:
    """ Class to normalize message """

    def __init__(self) -> None:
        self.names = ["mia", "Mia", "mia.", ",mia" "Mia,", "mia?", "Mia?"]

    def check_name_bot(self, message: str) -> bool:
        """
        Check if message contains name of bot
        """
        for name in self.names:
            if name in message:
                return True

        return False

    def normalize_message(self, message: str) -> str:
        """
        Normalize message
        """
        # Remove accents
        message = normalize('NFKD', message).encode('ASCII', 'ignore').decode('ASCII').lower()

        # Remove name of bot
        if self.check_name_bot(message):
            message = message.replace("mia", "")

        # Remove multiple spaces
        message = " ".join(message.split())

        return message
