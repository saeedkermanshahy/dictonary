from django.contrib import admin
from .models import Language, Source, Destination, Example


# Register your models here.
@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('src_lang', 'src_text')


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    pass


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    pass


@admin.register(Example)
class ExampleAdmin(admin.ModelAdmin):
    pass