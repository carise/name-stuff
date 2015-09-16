class Word(object):
  def __init__(self, word, phonemes=[], syllables):
    self.word = word
    self.phonemes = phonemes
    self.syllables = syllables

class WordParser(object):
  vowels = ['a', 'e', 'i', 'o', 'u']

  @classmethod
  def parse(cls, name):
    pass

