from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Language(models.Model):
    class ChooseLanguage(models.TextChoices):

        BG = "BG", "Bulgarian"
        CS = "CS", "Czech"
        DA = "DA", "Danish"
        DE = "DE", "German"
        EL = "EL", "Greek"
        EN_GB = "EN-GB", "British English"
        EN_US = "EN-US", "American English"
        ES = "ES", "Spanish"
        ET = "ET", "Estonian"
        FI = "FI", "Finnish"
        FR = "FR", "French"
        HU = "HU", "Hungarian"
        IT = "IT", "Italian"
        JA = "JA", "Japanese"
        LT = "LT", "Lithuanian"
        LV = "LV", "Latvian"
        NL = "NL", "Dutch"
        PL = "PL", "Polish"
        PT_PT = "PT-PT", "Portuguese"
        PT_BR = "PT-BR", "Brazilian Portuguese"
        RO = "RO", "Romanian"
        RU = "RU", "Russian"
        SK = "SK", "Slovak"
        SL = "SL", "Slovenian"
        SV = "SV", "Swedish"
        ZH = "ZH", "Chinese"

    src_lang = models.CharField(
        _("Source Language"),
        max_length=8,
        choices=ChooseLanguage.choices,
        default=ChooseLanguage.DE,
    )
    src_text = models.CharField(_("Source Text"), max_length=500)
    tar_text = models.CharField(_("Target Text"), max_length=500)
    tar_lang = models.CharField(
        _("Target Language"), max_length=8, choices=ChooseLanguage.choices
    )
    created_at = models.DateTimeField(
        _("Created At"), auto_now=False, auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _("Updated At"), auto_now=True, auto_now_add=False
    )

    class Meta:
        verbose_name = _("DeTranslation")
        verbose_name_plural = _("DeTranslations")

    def __str__(self):
        return self.src_text


class LingueeLanguages(models.TextChoices):
    BG = "bg", "Bulgarian"
    CS = "cs", "Czech"
    DA = "da", "Danish"
    EL = "el", "Greek"
    ES = "es", "Spanish"
    ET = "et", "Estonian"
    FI = "fi", "Finnish"
    FR = "fr", "French"
    HU = "hu", "Hungarian"
    IT = "it", "Italian"
    JA = "ja", "Japan"
    LT = "lt", "Lithuanian"
    LV = "lv", "Latvian"
    MT = "mt", "Maltese"
    NL = "nl", "Dutch"
    PL = "pl", "Polish"
    PT = "pt", "Portuguese"
    RO = "ro", "Romanian"
    RU = "ru", "Russian"
    SK = "sk", "Slovak"
    SL = "sl", "Solvene"
    SV = "sv", "Swedish"
    ZH = "zh", "Chinese"
    DE = "de", "German"
    EN = "en", "English"


class Source(models.Model):

    text = models.CharField(
        _("Source Text"), max_length=255, help_text="Words you want to translate"
    )
    pos = models.CharField(_("Pos"), max_length=255, null=True, blank=True)
    grammar_info = models.CharField(
        _("Grammar Info"), max_length=255, null=True, blank=True
    )
    featured = models.BooleanField(_("Featured"), null=True, blank=True)
    lang = models.CharField(
        _("Source Language"),
        max_length=8,
        choices=LingueeLanguages.choices,
        default=LingueeLanguages.DE,
    )

    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __str__(self):
        return self.text


class Destination(models.Model):

    text = models.CharField(_("Destination Text"), max_length=255)
    pos = models.CharField(_("Pos"), max_length=255, null=True, blank=True)
    featured = models.BooleanField(_("Featured"), null=True, blank=True)
    src = models.ForeignKey(
        "Source", verbose_name=_("Source"), on_delete=models.CASCADE
    )

    lang = models.CharField(
        _("Destination Language"), max_length=8, choices=LingueeLanguages.choices
    )

    class Meta:
        verbose_name = _("Translation")
        verbose_name_plural = _("Translations")

    def __str__(self):
        return self.text


class Example(models.Model):

    src_text = models.CharField(_("Source Example"), max_length=4096, null=True)
    dst_text = models.CharField(_("Destination Example"), max_length=4096, null=True)
    src = models.ForeignKey(
        "Source",
        verbose_name=_("Source"),
        on_delete=models.CASCADE,
        null=True,
        related_name="example",
    )
    dst = models.ForeignKey(
        "Destination",
        verbose_name=_("Destination"),
        on_delete=models.CASCADE,
        null=True,
        related_name="example",
    )

    class Meta:
        verbose_name = _("Example")
        verbose_name_plural = _("Examples")

    def __str__(self):
        return "Example"
