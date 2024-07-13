from .models import Message

class UnreadMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        unread_messages_count = Message.objects.filter(is_read=False).count()
        request.unread_messages_count = unread_messages_count
        response = self.get_response(request)
        return response