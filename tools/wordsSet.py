#!/usr/bin/env python3
import wordAttributes
import pickle
import re
import gzip

class WordSet(dict):
    SCRUB_RE = { "EN": r"[^a-zA-Z\s]",
                 "HE": r"[^א-ת\s\-]"}

    def __init__(self, lang_code = "En", scrub=True, *args, **kwargs):
        ''' Set scrub to True to remove special chars from word.
            The langCode is used to set a matching cleanup regular expression and must
            be provided if scrub is enabled.
        '''
        if scrub:
            if lang_code in WordSet.SCRUB_RE:
                self.scrubRe = re.compile(WordSet.SCRUB_RE[lang_code])
            else:
                raise ValueError(f"{self.__class__.__name__} scrub enabled for unknown language code")
        else:
            self.scrubRe = None
        
        super().__init__()
        
        # Very wastefull, but if overriding __setitem__ leaving this not handled looks bad.
        for key, value in dict(*args, **kwargs).items():
            self[key]=value # Force going through __setitem__

    def __setitem__(self, word, attributes):
        ''' Attribues are either as int vaue or AttributeFlags Enum values.
            If none provided Set to None detect attibute abbrevations within word string.
            If set to 0 no attribute abbrivations are expected.
        '''
        if not hasattr(self, "scrubRe"):
            # We got here through un-pickle, it first restores the dict, use the values as they are
            # don't let it progress beyond this as other class members have not been restored yet!
            super().__setitem__(word, attributes)
            return

        if not isinstance(word, str):
            raise TypeError(f"{self.__class__.__name__} key must be strings")
        
        word = word.strip()
        if not word:
            raise ValueError(f"{self.__class__.__name__} key must not be empty string!")

        word_info = word.split('(')
        if len(word_info) == 1 and self.scrubRe:
            word = self.scrubRe.sub("", word)

        if attributes:
            if not isinstance(attributes, int) and not isinstance(attributes, wordAttributes.AttributeFlags):
                raise TypeError(f"{self.__class__.__name__} value must be file attribute as int or WordAttributesFlags")
            if len(word_info) > 1:
                raise TypeError(f"{self.__class__.__name__} word attributes must be supplied either value or embedded in word, not both")

            if isinstance(attributes, wordAttributes.AttributeFlags):
                attributes = attributes.value
            
            super().__setitem__(word, attributes)

        elif len(word_info) == 1:
            super().__setitem__(word, 0) # Word, no attributes
        else:
            # Need to parse word attributes
            # expected format: `<word> (<attribues1, attribute2, ...>) (<language locale>)
            # Here we know we have at least two parts to the word
            attributes = wordAttributes.AttributeFlags(0)
            for i in range(1, len(word_info)):
                attribute_abbrevs = word_info[i].split(",")
                for abbrev in attribute_abbrevs:
                    abbrev = abbrev.strip(" )")
                    # Will raise excption if value is not know attribue abbrevation
                    attributes |= wordAttributes.abbrev_to_flag(abbrev)
            
            if self.scrubRe:
                word = self.scrubRe.sub("", word_info[0])
            else:
                word = word_info[0]

            super().__setitem__(word, attributes.value)

    @classmethod
    def dumpWordset(cls, word_set, file_path):
        ''' gzip pickle to file
        '''
        with gzip.open(file_path, 'wb') as gfile:
            pickle.dump(word_set, gfile)
    
    @classmethod
    def loadWordSet(cls, file_path):
        ''' load from previously gzip pickled content in file
            Will raise TypeError if content in file is not of this class
        '''
        with gzip.open(file_path, 'rb') as gfile:
            loaded_set = pickle.load(gfile)
            print(f"Loaded object type: {type(loaded_set)}")
        if not isinstance(loaded_set, cls):
            raise TypeError(f"{cls.__name__} Loaded is not of self type!")
        return loaded_set
    
    @classmethod
    def fromTextFile(cls, lang_code, file_path):
        newSet = WordSet(lang_code)
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    break
                abbrev_item = line.split(":")
                if len(abbrev_item) == 1:
                    # This is the first word. Add it and breal
                    newSet[line] = None
                else:
                    # Validate we know all abbrivations used in this file
                    abbrev, _ = abbrev_item
                    abbrev = abbrev.replace(" ", "_")
                    if abbrev not in wordAttributes.Abbrev:
                        raise ValueError(f"{cls.__name__} Unknon Attribte abbrivation: {line}")
            # The rest are expected to be words
            for line in f:
                line = line.strip()
                if not line:
                    break
                newSet[line] = None
        return newSet

if __name__ == "__main__":
    import argparse
    from os import path

    parser = argparse.ArgumentParser(description="Convert text word list to compressed pyton word setof type WordSet",
                                     epilog='''File format: Can start with abbrevation list in format <abbrev>:<Full text meaning>
                                     followed by the words, word per line. The words can have additional attribute content
                                     matching the abbrivation specified int the format: <word> (<attrib1>, <attrib2>...)
                                       (<attribA, AttribB) where the second group of attribues is typically local language
                                       identifier 
                                     ''')
    parser.add_argument('-l', '--langcode', default="EN", help="Two letter languae identifier")
    parser.add_argument('file', help="Full path to text file with word list, or gz pickled file for load testing")
    parser.add_argument('-t', '--test', action="store_true", help="Load and repost set size of .pkl.gz file")

    args = parser.parse_args()
    if args.test:
        wordSet = WordSet.loadWordSet(args.file)
        print(f"Word set loaded with {len(wordSet)} words")
        print("Test adding entry 'TestValue!@' with attribute 33")
        wordSet["TestValue!@"] = 33
        print(f"Word set loaded with {len(wordSet)} words")
        print("Read the scrubbed word entry 'TestValue'")
        print(wordSet["TestValue"])
        exit(0)
        
    wordSet = WordSet.fromTextFile(args.langcode, args.file)
    print(f"Word set loaded with {len(wordSet)} words")
    base_name, _ = path.splitext(args.file)
    file_path = base_name + ".pkl.gz"
    WordSet.dumpWordset(wordSet, str(file_path))
    print(f"Dumped to file: {file_path}")
