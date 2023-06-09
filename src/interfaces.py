

class IntegrationBot:
    """ Integration Bot """

    async def thinking(self):
        """ Thinking """
        pass

    ### COMMANDS ###

    async def send_message(self, chat_id, message):
        """ 
        ### Send message

        :param chat_id: Channel ID or User ID
        :parm message: Message

        :return: Message ID 
        """
        pass

    async def send_reply(self, chat_id, message, reply_message_id):
        """ Send reply message """
        pass

    async def send_photo(self, chat_id, photo, message=None, private=False):
        """
        ### Send photo to DM or channel

        :param chat_id: Channel ID or User ID
        :param photo: Photo path
        :param message: Message
        :param private: Send to DM

        :return: Message ID
        """
        pass

    async def send_git(self, chat_id, gif, message=None):
        """ Send gif """
        pass

    async def send_action(self, chat_id):
        """ 
        ### Send action typing in chat 

        :param chat_id: Channel ID or User ID

        :return: Message ID
        """
        pass

    def run(self):
        """ Running bot """
        pass
