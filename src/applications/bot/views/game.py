import json
import traceback
from typing import Dict

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from applications.bot.rules.custom_types import MessageT
from applications.bot.rules.fsm import get_handler
from applications.bot.rules.utils import respond_to_telegram


@method_decorator(csrf_exempt, name="dispatch")
class GameView(View):
    def post(self, *args, **kw):
        try:
            handler = get_handler(self.message)
            text_response = handler(self.message)
            respond_to_telegram(self.message.chat_id, text_response)

        except Exception:
            traceback.print_exc()

        return HttpResponse(status=200)

    @property
    def message(self) -> MessageT:
        update: Dict = json.loads(self.request.body)
        message: Dict = update["message"]
        text: str = message["text"]
        chat: Dict = message["chat"]
        chat_id: str = chat["id"]

        result = MessageT(chat_id=chat_id, text=text)
        return result
