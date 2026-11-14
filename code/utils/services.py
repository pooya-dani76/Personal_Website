


def get_lang(request):
    raw = request.query_params.get("lang") or request.headers.get("Accept-Language", "fa")
    return "en" if raw.lower().startswith("en") else "fa"

def lf(*names):
    """lf("name", "role") -> ["name_fa", "name_en", "role_fa", "role_en"]"""
    return [f"{n}_{lang}" for n in names for lang in ("fa", "en")]

def success_message(info_name_en, info_name_fa, lang):
    return f"{info_name_en} Retrived Successfully" if lang=="en" else f"{info_name_fa} با موفقیت بازگردانده شد"