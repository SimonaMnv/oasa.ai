import re


def replace_last(source_string, replace_what, replace_with):
    head, _sep, tail = source_string.rpartition(replace_what)
    return head + replace_with + tail


word = "ΑΓ. ΝΙΚΟΛΑΛΑ"

k = re.search("[ΟΣ]{2}$", word)  # match last 2 characters
if k:
    r = replace_last(word, 'ΑΓ.', 'ΑΓΙΟΣ')
    print(r)