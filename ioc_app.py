from os import listdir
import sys
from ioc import DELTA, PT_ETAOIN, find_most_likely_language, ioc_by_key_length, get_vigenere_key, decrypt_vigenere, decrypt_by_letter_frequency


def main(): 
  dir_texts = 'encrypted'
  key_computation_limit = 15
  
  output_res = []
  
  for file_name in listdir(dir_texts):
    path = f'{dir_texts}/{file_name}'
    text = read_file(path)
    print(path)

    results = ioc_by_key_length(text, key_computation_limit)
    best_ioc = max([res['ioc'] for res in results])
    best = next(res for res in results if abs(res['ioc'] - best_ioc) < DELTA)
    print(f"Best result: Key Length: {best['key_length']}, IoC:{best['ioc']}")
    
    language_stats = find_most_likely_language(best['ioc'])
    
    #key = get_vigenere_key(best['counts'], language_stats['etaoin'])
    key = get_vigenere_key(best['counts'], 'e')
    print('key:', key)
    
    # Decryption sample for the first 200 characters
    dec_sample = decrypt_vigenere(text[0:200], key)
    
    print('decrypted sample:')
    print(dec_sample)
    
    # Text analysis using substitution by frequency
    # print(decrypt_by_letter_frequency(text[0:200], best['counts'], PT_ETAOIN))
    
    print()
    
    output_res.append({'file':file_name,
                       'ioc':best['ioc'],
                       'language': language_stats['language'],
                       'key':key,
                       'dec sample':dec_sample})
  
  output_to_file(output_res)

def read_file(path):
  file = open(path)
  text = file.read()
  file.close()
  return text

def output_to_file(output_res):
  output_file = open('vigenere_decryption_results.txt', 'w')
  for res in output_res:
    output_file.write('===============================================================\n')
    output_file.write(f"file: {res['file']}\nioc: {res['ioc']}\nlanguage: {res['language']}\nkey: {res['key']}\ndecryption sample: {res['dec sample']}\n\n")
  
  output_file.close()
  
if __name__ == "__main__":
  main()
