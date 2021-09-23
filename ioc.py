from os import listdir
from io import StringIO


#==================================================================================================
# CONSTANTS

ABC        = 'abcdefghijklmnopqrstuvwxyz'

# Index of coincidence for Portuguese and English
# Source: https://en.wikipedia.org/wiki/Index_of_coincidence
PT_IOC     = 1.94
EN_IOC     = 1.73

# Etaoin refers to the sequence of characters ordered by frequency in a given language
# Source: https://pt.wikipedia.org/wiki/Frequ%C3%AAncia_de_letras
PT_ETAOIN  = 'aeosrindmutclpvghqbfzjxkwy'
EN_ETAOIN  = 'etaoinshrdlcumwfgypbvkjxqz'

# The index of coincidence for a key length tends to be similar for multiples of that key length.
# Example: if the key length for a vigenere encryption is 4, the calculated IoC for a key length of 8 
# will be just as good or even better.
# Given that it is highly unlikely that subsequent multiples of the first best result are the correct 
# ones, the first result whose difference to the best result is lower than DELTA is chosen as the 
# correct key length.
DELTA      = 0.001



#==================================================================================================
#FUNCTIONS

# Computes index of coincidence for each key length in a range.
# Function arguments:
  # text: encrypted text.
  # max_key_len: Arbitrary value. The function won't compute index of coincidence for keys larger than this argument.
# Returns: list of dictionaries [{key_length, ioc, counts}]
  # key_length: key length.
  # ioc: corresponding index of coincidence.
  # counts: corresponding dictionary of letters and how many times they appear in a text section.
def ioc_by_key_length(text, max_key_len):
  
  results = []
  
  for i in range(1, max_key_len+1):
    # Divides the text in a number of sections equal to the assumed key length i
    print(f'Dividing text in {i} sections...')
    sections = divide_text_in_sections(text, i)
    
    # Computes average index of coincidence for all sections
    total_ioc = 0
    char_counts = []
    print('Calculating ioc...')
    for s in sections:
      (ioc, char_count) = index_of_coincidence(s)
      char_counts.append(char_count)
      total_ioc += ioc
      
    results.append({'key_length':i, 'ioc':total_ioc/i, 'counts':char_counts})
    print(f'Result for key length {i}: {total_ioc/i}')
    print('Done\n===========================================================\n\n')
  return results


def divide_text_in_sections(text, n):
  sections = [StringIO() for i in range(n)]
  for i, c in enumerate(text):
    sections[i%n].write(c)
  return [s.getvalue() for s in sections]


# Returns index of coincidence and character count for a given text
def index_of_coincidence(text):
  counts = {c:0 for c in ABC}
  
  for c in text:
    counts[c] += 1
    
  n = len(text)
  ioc = sum([v * (v-1) for v in counts.values()]) / ((n * (n-1)) / len(ABC))
  return (ioc, counts)


# Attempts text decryption by substituting each character in a section with it's
# corresponding character in the language based on frequency. Used for text analysis.
def decrypt_by_letter_frequency(text, char_counts, etaoin):
  res = StringIO()
  n_sections = len(char_counts)
  #print('char_counts:')
  #for cc in char_counts:
    #print(sorted(cc.items(), reverse=True, key=(lambda t: t[1])))
  substitution_dicts = []
  for cc in char_counts:
    cc_sorted = [k for (k,v) in rev_sorted_items(cc)]    #t = (char, count)
    substitution_dicts.append( dict(zip(cc_sorted, etaoin)) )
  # for sd in substitution_dicts:
    # print(sd)
  for i, c in enumerate(text):
    substitute_char = substitution_dicts[i%n_sections][c]
    res.write(substitute_char)
  
  return res.getvalue()


# Finds the vigenere encryption key given the character counts of each
# text section and the alphabet ordered by character frequency in the language
def get_vigenere_key(char_counts, etaoin):
  # Most frequent char in language
  dec = etaoin[0]
  key = StringIO()
  for cc in char_counts:
    sorted_chars = rev_sorted_items(cc)
    # Most frequent encrypted char for that section
    enc = sorted_chars[0][0]
    key.write( subtract_char(enc, dec) )
  return key.getvalue()

  
def decrypt_vigenere(text, key):
  res = StringIO()
  key_length = len(key)
  for i, c in enumerate(text):
    res.write(subtract_char(c, key[i%key_length]))
  return res.getvalue()


def encrypt_vigenere(text, key):
  res = StringIO()
  key_length = len(key)
  for i, c in enumerate(text):
    res.write(add_char(c, key[i%key_length]))
  return res.getvalue()


# Returns most likely language based on index of coincidence
def find_most_likely_language(ioc):
  language_stats = [
    {'language': 'English',    'ioc': EN_IOC, 'etaoin': EN_ETAOIN},
    {'language': 'Portuguese', 'ioc': PT_IOC, 'etaoin': PT_ETAOIN}
  ]
  
  best_score = 9999
  res = None
  for stats in language_stats:
    difference = abs(stats['ioc'] - ioc)
    if difference < best_score:
      res = stats
      best_score = difference
  
  return res


def subtract_char(c1, c2):
  res_ord = ord(c1)-ord(c2)
  res_ord = (res_ord%len(ABC)) + ord('a')
  return chr(res_ord)


def add_char(c1, c2):
  res_ord = ord(c1)+ord(c2) - 2*ord('a')
  res_ord = (res_ord%len(ABC)) + ord('a')
  return chr(res_ord)


# Takes a dictionary {k:v} and returns a list [(k,v)] reverse sorted by v
def rev_sorted_items(dictionary):
  return sorted(dictionary.items(), reverse=True, key=(lambda t: t[1]))



if __name__ == "__main__":
  main()
  
  
  
  
  
  