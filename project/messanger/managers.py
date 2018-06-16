from django.db.models import Manager

class ConversationManager(Manager):
    def get_or_create_conversation(self, profile, profiles):
        for conversation in profile.conversation_set.all():
            if set(list(conversation.profiles.all())) == set(profiles):
                return conversation
        conversation = self.create()
        conversation.profiles = profiles
        return conversation

    def unread_messages_count(self, profile):
        count = 0
        for c in profile.conversation_set.all():
            count += c.get_unread_messages(profile).count()
        return count

    def get_conversations_to_read(self, profile):
        to_read = []
        for c in profile.conversation_set.all():
            if c.get_unread_messages(profile).count() > 0:
                to_read.append(c)
        return to_read

