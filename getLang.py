from langs import en, it

lang_obj = {
    "en": en,
    "it": it,
}


def getString(lang, variable):
    """
    returns the right string. example of usage:
    print(get_string("en", "test"))
    'en' is the language of the user returned from the db
    '"test"' is the name of the variable in the relative file lang
    """

    try:
        string = getattr(lang_obj[lang], variable)
    except AttributeError:
        string = getattr(en, variable)
    except KeyError:
        string = getattr(en, variable)
    return string


def getStringButtons(lang, variable):
    try:
        dct = getattr(lang_obj[lang], 'buttons_strings')
    except AttributeError:
        dct = getattr(en, 'buttons_strings')
    except KeyError:
        dct = getattr(en, 'buttons_strings')
    return dct[variable]