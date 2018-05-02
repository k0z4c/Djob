from django.db.models import Manager

class ConversationManager(Manager):
    def get_or_create_conversation(self, user, users):
        for conversation in user.conversation_set.all():
            if set(list(conversation.users.all())) == set(users):
                return conversation
        conversation = self.create()
        conversation.users = users
        return conversation

    def unread_messages_count(self, user):
        count = 0
        for c in user.conversation_set.all():
            count += c.get_unread_messages(user).count()
        return count

    def get_conversations_to_read(self, user):
        to_read = []
        for c in user.conversation_set.all():
            if c.get_unread_messages(user).count() > 0:
                to_read.append(c)
        return to_read

