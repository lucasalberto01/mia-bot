

class IntegrationBot:
    """ Integration Bot """

    async def send_message(self, chat_id, message):
        """ Send message """
        pass

    async def send_reply(self, chat_id, message, reply_message_id):
        """ Send reply message """
        pass

    async def send_photo(self, chat_id, photo, message=None):
        """ Send photo """
        pass

    async def send_action(self, chat_id):
        """ Send action typing in chat """
        pass

    def running(self):
        """ Running bot """
        pass
