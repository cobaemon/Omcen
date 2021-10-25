from django.contrib import admin

from password_box.models import PasswordBoxUser, PasswordBoxTag, PasswordBox, PasswordBoxNonce

admin.site.register(PasswordBoxUser)
admin.site.register(PasswordBox)
admin.site.register(PasswordBoxTag)
admin.site.register(PasswordBoxNonce)
