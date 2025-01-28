#!/usr/bin/env python3
from enum import Flag, auto

# Python 3.7+ dict preserve order. Otherwise use ordered dictionary
WordAttribuesAbbrev = {
        ''' Using Abbreviations adopted from Cambridge Vocabulary listing.
            Language locale changed to IETF BCP 47 identifiers.
            Try to keep this limited to 32 values.
        '''
        "n":"noun",
        "v":"verb",
        "adj":"adjective",
        "av":"adverb",
        "av":"auxiliary verb",
        "conj":"conjunction",
        "det":"determiner",
        "exclam":"exclamation",
        "det":"determiner",
        "phrv":"phrasal verb",
        "pron":"pronoun",
        "prep":"preposition",
        "prep_phr":"prepositional phrase",
        "pl":"plural",
        "sing":"singular",
        "r1":"reserved",
        "r2":"reserved",
        "r3":"reserved",
        "r4":"reserved",
        "r5":"reserved",
        "r6":"reserved",
        "r7":"reserved",
        "en_US":"American/US English",
        "en_GB":"British English",
    }

# Using flag to get bitwise separate entries.
WordAttributesFlags = Flag('WordAttributesFlags', {key.replace(" ", "_"): auto() for key in WordAttribuesAbbrev})

def Word_attribute_to_text(flag:WordAttributesFlags)->str:
    ''' For given attribute flag from WordAttributesFlags
        return the full attribute text description
    '''
    if not isinstance(flag, WordAttributesFlags):
        raise TypeError(f"Expected a Flag type, got {type(flag).__name__}")
    
    return WordAttributesFlags[flag.name]

def Word_attribute_abbrev_to_flag(abbrev:str):
    ''' For a word abbreviation string return the assigned enumeration flag.
        Will raise ValueError if abbreviation is not from list in WordAttribuesAbbrev.
    '''
    abbrev = abbrev.replace(" ", "_") # allow space in abbreviation, but in flag we had to replace it
    try:
        return WordAttributesFlags[abbrev] # access the flag directly
    except KeyError:
        raise ValueError(f"Abbrivation '{abbrev}' is not valid.")
