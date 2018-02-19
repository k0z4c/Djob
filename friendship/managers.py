from django.db import models

class FriendshipRequestManager(models.Manager):
    def send_request(self, by, to):
        request = self.filter(by=by, to=to)
        if request:
            return None
        request = self.create(by=by, to=to)
        return request

class FriendshipManager(models.Manager):
    def is_friend(self, us1, us2):
        try:
            self.get(by=us1, to=us2)
        except self.model.DoesNotExist:
            return False
        return True

    def add_friend(self, us1, us2):
        pass
