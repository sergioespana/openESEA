from django.contrib import admin
from .models import (
    User,
    Organization,
    Method,
    Question,
    DirectIndicator,
    IndirectIndicator,
    QuestionOption,
)

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(Method)
admin.site.register(DirectIndicator)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(IndirectIndicator)
