import django.dispatch

# providing_args: declares parameters passed to receiver func; e.g. instance 
social_request_accepted = django.dispatch.Signal(providing_args=[])
social_request_rejected = django.dispatch.Signal(providing_args=[])
