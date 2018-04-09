from django.forms.utils import ErrorList

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        return '<div class="errorlist">{}</div>'.format(
            ''.join(
                [ '<div class="error">{}</div>'.format(e) for e in self]
                )
            )
   