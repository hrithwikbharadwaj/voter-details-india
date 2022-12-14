from google.cloud import translate
import os


def translate_text(english_path: str, text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'keys.json'
    project_id = os.getenv('PROJECT_ID')
    client = translate.TranslationServiceClient()
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": "kn",
            "target_language_code": "en-US",
        }
    )

    for translation in response.translations:

        f = open(english_path, "a", encoding="utf-8")

        lines = translation.translated_text.split("\n")

        string_without_empty_lines = ""

        for line in lines:
            string_without_empty_lines += line + "\n"

        f.write(string_without_empty_lines)
        f.close()


def translate_locale_out(locale_path: str, english_path: str):
    tamil_text = ""

    with open(locale_path, 'r', encoding="utf8") as file:

        line = file.readline()
        cnt = 1
        while line:
            tamil_text = tamil_text + line
            cnt += 1
            line = file.readline()

    l = len(tamil_text)

    while l > 0:
        if l > 30000:
            translate_text(english_path, tamil_text[:30000])
            tamil_text = tamil_text[30000:]
            l = len(tamil_text)
        else:
            translate_text(english_path, tamil_text)
            l = 0


# translate_locale_out("localOutput.txt", "englishOutPut.txt")
