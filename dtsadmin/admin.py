# coding:UTF-8
from django.contrib import admin

# Register your models here.
from .models import Informations, ConsultFeedback



class InformationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'info_type', 'name', 'content', 'order_no', 'info_status', 'start_date', 'end_date'
                    , 'update_user', 'update_date', 'reviewer', 'review_date', 'is_top', 'audience'
                    )

admin.site.register(Informations, InformationsAdmin)


class ConsultFeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'feedback_type', 'created', 'is_display', 'is_replied', 'updated', 'replied_content', )

admin.site.register(ConsultFeedback, ConsultFeedbackAdmin)
