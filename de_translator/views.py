from django.shortcuts import render
from .models import Language, Source, Destination, Example
from .forms import LanguageForm, LingueeSourceForm
from django.conf import settings
from django.forms.models import model_to_dict

import requests
import deepl
import logging
import json

logging.basicConfig(
    filename="logs.log",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)
logging.getLogger("deepl")

# Create your views here.
def de_translator(request):
    form = LanguageForm(request.GET)
    result = None
    src_text = None
    if form.is_valid():
        # Use DeepL Libraty
        translator = deepl.Translator(settings.DEEPL_AUTH_KEY)
        translations = Language.objects.filter(
            src_text=form.cleaned_data["src_text"],
            tar_lang=form.cleaned_data["tar_lang"],
        ).first()

        if translations is None:
            result = translator.translate_text(
                form.cleaned_data["src_text"], target_lang=form.cleaned_data["tar_lang"]
            )
            saved_form = form.save(commit=False)

            saved_form.tar_text = result.text
            saved_form.save()
        else:
            result = translations.tar_text
        
        src_text = form.cleaned_data["src_text"]

    return render(
        request,
        "translate.html",
        {"form": form, "result": result, "src_text": src_text},
    )


def linguee(request):
    form = LingueeSourceForm(request.GET)
    result = None
    status_code = 200

    if form.is_valid():
        # Use Linguee API

        destinations = Destination.objects.filter(
            lang=form.cleaned_data["dst_lang"],
            src__text=form.cleaned_data["source_text"],
            src__lang="de",
        )

        if destinations.first() is None:
            api_root = "https://linguee-api-v2.herokuapp.com/api/v2"
            resp = requests.get(
                f"{api_root}/translations",
                params={
                    "query": form.cleaned_data["source_text"],
                    "src": "de",
                    "dst": form.cleaned_data["dst_lang"],
                },
            )

            try:
                result = json.loads(resp.text)[0]

                source = Source.objects.create(
                    text=result["text"],
                    pos=result.get("pos"),
                    featured=result.get("featured"),
                    grammar_info=result.get("grammar_info"),
                    lang="de",
                )

                for translation in result["translations"]:
                    destination = Destination.objects.create(
                        text=translation["text"],
                        featured=True,
                        pos=translation["pos"],
                        src=source,
                        lang=form.cleaned_data["dst_lang"],
                    )

                    if translation.get("examples") is not None:
                        if len(translation.get("examples")) > 0:

                            for example in translation["examples"]:
                                example = Example.objects.create(
                                    src_text=example["src"],
                                    dst_text=example["dst"],
                                    src=source,
                                    dst=destination,
                                )

            except Exception:
                print("No Translation Found")
                status_code = resp.status_code
                result = False

        else:
            destinations = Destination.objects.filter(
                lang=form.cleaned_data["dst_lang"],
                src__text=form.cleaned_data["source_text"],
                src__lang="de",
            )
            source = destinations.first().src
            source_dict = model_to_dict(source)
            source_dict.pop("id")
            source_dict.pop("lang")

            source_dict["translations"] = []

            for destination in destinations:
                destination_dict = model_to_dict(destination)
                destination_dict.pop("id")
                destination_dict.pop("lang")
                destination_dict.pop("src")

                destination_dict["examples"] = []

                examples = Example.objects.filter(src=source, dst=destination)

                for example in examples:
                    example_dict = model_to_dict(example)
                    destination_dict["examples"].append(
                        {
                            "src": example_dict["src_text"],
                            "dst": example_dict["dst_text"],
                        }
                    )

                source_dict["translations"].append(destination_dict)

            result = source_dict

    return render(
        request,
        "translate.html",
        {"form": form, "result": result, "linguee": True, "status_code": status_code},
    )
