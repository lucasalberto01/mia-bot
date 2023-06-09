"""Thisfilecontainsthedefault(English) substitutions for the
PyAIML kernel.  These substitutions may be overridden by using the
Kernel.loadSubs(filename) method.  The filename specified should refer
to a Windows-style INI file with the following format:

    # lines that start with '#' are comments

    # The 'gender' section contains the substitutions performed by the
    # <gender> AIML tag, which swaps masculine and feminine pronouns.
    [gender]
    he = she
    she = he
    # and so on...

    # The 'person' section contains the substitutions performed by the
    # <person> AIML tag, which swaps 1st and 2nd person pronouns.
    [person]
    I = you
    you = I
    # and so on...

    # The 'person2' section contains the substitutions performed by
    # the <person2> AIML tag, which swaps 1st and 3nd person pronouns.
    [person2]
    I = he
    he = I
    # and so on...

    # the 'normal' section contains subtitutions run on every input
    # string passed into Kernel.respond().  It's mainly used to
    # correct common misspellings, and to convert contractions
    # ("WHAT'S") into a format that will match an AIML pattern ("WHAT
    # IS").
    [normal]
    what's = what is
"""

defaultGender = {
    # masculine -> feminine
    "ele": "ela",
    "ele": "ela",
    "dele": "ela",
    "ele mesmo": "ela mesma",

    # feminine -> masculine
    "ela": "ele",
    "ela": "ele",
    "dela": "dele",
    "ela mesma": "ele mesmo",
}

defaultPerson = {
    # 1st->3rd (masculine)
    "eu": "ele",
    "eu": "ele",
    "meu": "dele",
    "meu": "dele",
    "eu mesmo": "ele mesmo",

    # 3rd->1st (masculine)
    "ele": "eu",
    "ele": "eu",
    "dele": "meu",
    "ele mesmo": "eu mesmo",

    # 3rd->1st (feminine)
    "ela": "eu",
    "ela": "eu",
    "dela": "meu",
    "ela mesma": "eu mesmo",
}

defaultPerson2 = {
    # 1st -> 2nd
    "eu": "você",
    "eu": "você",
    "meu": "seu",
    "meu": "seu",
    "eu mesmo": "você mesmo",

    # 2nd -> 1st
    "você": "eu",
    "seu": "meu",
    "seu": "meu",
    "você mesmo": "eu mesmo",
}


# TODO: this list is far from complete
defaultNormal = {
    # de -> para
    'voce': 'vc',
    'nudez': 'nude',
    'privado': 'pv',
    'pvd': 'pv',
    'obrigado': 'obg',
    'brigado': 'obg',
    'ond': 'onde',
    'aonde': 'onde',
    'zap': 'wpp',
    'whatsapp': 'wpp',
    'wts': 'wpp',
    'ft': 'foto',
    'peitos': 'tetas',
    'peito': 'tetas',
    'teta': 'tetas',
    'tc': 'fala',
    'vamos': 'vamo',
    'foda-se': 'fodase',
    'fds': 'fodase',
    'nois': 'nos',
    'comigo': 'cmg',
    'vai se foder': 'vsf',
    'vsfd': 'vsf',
}
