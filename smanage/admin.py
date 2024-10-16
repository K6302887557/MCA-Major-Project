from django.contrib import admin
from .models import CustomUser, UploadedFile
from django.utils.html import format_html
from django.utils.crypto import get_random_string

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'generate_key')  # Customize the fields displayed in the admin list view
    search_fields = ('username', 'email')  # Add fields for searching
    list_filter = ('is_staff', 'is_active')  # Add filters for the list view
    readonly_fields = ('generate_key',) #add this line to make the generate_key filed read-only

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.generate_key:  # New user being created
            obj.generate_key = form.cleaned_data['generate_key']  # Set the entered key value
        return super().save_model(request, obj, form, change)


admin.site.unregister(CustomUser)

admin.site.register(CustomUser, CustomUserAdmin)



class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('display_file', 'uploaded_by')

    def display_file(self, obj):
        # Return a formatted HTML link with the file name
        return format_html('<a href="{}">{}</a>', obj.file.url, obj.file.name)

    display_file.short_description = 'File'

    def uploaded_by(self, obj):
        # Return the username of the user who uploaded the file
        return obj.user.username

    uploaded_by.short_description = 'Uploaded By'

# Register the model and the custom admin class
admin.site.register(UploadedFile, UploadedFileAdmin)