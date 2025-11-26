from django.contrib import admin

from toasty.aibot.db_models import AibotComment, GithubAppInstallation, GithubAppRepo

admin.site.register(GithubAppInstallation)
admin.site.register(GithubAppRepo)
admin.site.register(AibotComment)
