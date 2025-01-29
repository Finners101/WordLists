#!/usr/bin/env python3
from enum import Flag, auto

# Python 3.7+ dict preserve order. Otherwise use ordered dictionary
''' Using Abbreviations adopted from Cambridge Vocabulary listing.
    Language locale changed to IETF BCP 47 identifiers.
    Limited this to 32 values to have the attribute value HEX at 32 bit int
'''
Abbrev = {
        "n":"noun",
        "v":"verb",
        "adj":"adjective",
        "adv":"adverb",
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
        "pn":"proper noun",
        "mv":"Modal Verb",
        "r15":"reserved",
        "r14":"reserved",
        "r13":"reserved",
        "r12":"reserved",
        "r11":"reserved",
        "r10":"reserved",
        "r9":"reserved",
        "r8":"reserved",
        "r7":"reserved",
        "r6":"reserved",
        "r5":"reserved",
        "r4":"reserved",
        "r3":"reserved",
        "r2":"reserved",
        "r1":"reserved",
        "en_US":"American/US English",
        "en_GB":"British English",
    }

# Using flag to get bitwise separate entries.
AttributeFlags = Flag('AttributeFlags', {key.replace(" ", "_"): auto() for key in Abbrev})

def flag_to_text(flag:AttributeFlags)->str:
    ''' For given attribute flag from WordAttributesFlags
        return the full attribute text description
    '''
    if not isinstance(flag, AttributeFlags):
        raise TypeError(f"Expected a Flag type, got {type(flag).__name__}")
    
    return AttributeFlags[flag.name]

def abbrev_to_flag(abbrev:str):
    ''' For a word abbreviation string return the assigned enumeration flag.
        Will raise ValueError if abbreviation is not from list in WordAttribuesAbbrev.
    '''
    abbrev = abbrev.replace(" ", "_") # allow space in abbreviation, but in flag we had to replace it
    try:
        return AttributeFlags[abbrev] # access the flag directly
    except KeyError:
        raise ValueError(f"Abbrivation '{abbrev}' is not valid.")
