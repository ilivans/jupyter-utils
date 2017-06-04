from __future__ import print_function

import telepot
import time
import sys


class TelegramLogger:
    def __init__(self, bot_token, chat_id):
        """Builds bot instance. Writes status message. 
        :param bot_token: Bot's token (details: https://core.telegram.org/bots/faq#how-do-i-create-a-bot).
        :param chat_id: ID of the chat where bot will write (details: https://stackoverflow.com/a/32572159/4229825).
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self._bot = telepot.Bot(self.bot_token)
        try:
            res = self._bot.getMe()
            self.__bot_name = res['username']
            self.__bot_id = res['id']
            print('{} (id{}) successfully created.'.format(self.__bot_name, self.__bot_id), file=sys.stderr)
        except telepot.exception.TelegramError as exception:
            print('Error while creating a bot.\n', exception, file=sys.stderr)

    def log(self, message, timeout=None, disable_notification=False, parse_mode=None):
        """
        Sends message to the bot.
        :param message: Message text.
        :param timeout: Time in seconds during which bot will try to send the message. If None it will try once.
        :param disable_notification: Indicator of notification disabling.
        :param parse_mode: Formatting mode: "HTML" or "Markdown" 
            (details: https://core.telegram.org/bots/api#formatting-options).
        """
        if parse_mode:
            assert parse_mode in ['Markdown', 'HTML'], 'Invalid parse_mode value.' \
                                                       'Only "Markdown" and "HTML"' \
                                                       'are available.'

        if not timeout:
            try:
                self._bot.sendMessage(self.chat_id,
                                      message,
                                      disable_notification=disable_notification,
                                      parse_mode=parse_mode)
            except telepot.exception.TelegramError as exception:
                print('Error while sending a message.\n', exception,
                      file=sys.stderr)

        else:
            start_time = time.time()
            while True:
                try:
                    self._bot.sendMessage(self.chat_id,
                                          message,
                                          disable_notification=disable_notification,
                                          parse_mode=parse_mode)
                    break
                except telepot.exception.TelegramError as exception:
                    if time.time() - start_time >= timeout:
                        print('Timeout exceed. Error while sending a message.\n',
                              exception, file=sys.stderr)
                        break

    def __repr__(self):
        return '{}. Bot name: {}. Bot id: {}. Chat id: {}'.format(
            self.__class__.__name__,
            self.__bot_name,
            self.__bot_id,
            self.chat_id)
