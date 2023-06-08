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
        Normalize message to remove name of bot
        """
        msg1 = normalize('NFKD', message).encode(
            'ASCII', 'ignore').decode('ASCII').lower()
        msg1 = ' ' + msg1

        replacements = {
            ' voce': ' vc',
            'mia ': '',
            ' mia ': '',
            ' mia': '',
            ' nudez': ' nude',
            ' privado': ' pv',
            ' pvd': ' pv',
            ' obrigado': ' obg',
            ' brigado': ' obg',
            ' ond': ' onde',
            ' aonde': ' onde',
            ' zap': ' wpp',
            ' whatsapp': ' wpp',
            ' wts': ' wpp',
            ' ft': ' foto',
            ' peitos': ' tetas',
            ' peito': ' tetas',
            ' teta': ' tetas',
            ' tc': ' fala',
            ' vamos': ' vamo',
            ' foda-se': ' fodase',
            ' fds': ' fodase',
            ' nois': ' nos',
            ' comigo': 'cmg'
        }

        for old, new in replacements.items():
            msg1 = msg1.replace(old, new)

        if message in ('mia', 'MIA'):
            msg1 = 'mia'

        return msg1
