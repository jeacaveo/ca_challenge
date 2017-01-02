from django.contrib import admin
from consumers import models


class ReviewAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.Review, ReviewAdmin)
admin.site.register(models.Company, CompanyAdmin)
