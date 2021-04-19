#!/usr/bin/env python3

import text_stats as ts
import random
import sys

def text_generator(txt_file, startword, maxwords):
    
    text_str = ts.file_input(txt_file)
    cleaned_txt = ts.clean_data(text_str)
    
    sub_seq_words = ts.subsequent_words(filtered_txt = cleaned_txt, target_words = None, all_the_words = True)
    
    cur_word = startword
    msg = ''
    
    for i in range(maxwords):
        msg = msg + " " + cur_word    
        cw = sub_seq_words[cur_word]
        if cw is None:
            break
        else:
            #Find the weights by first find the total times a word is a successor of cur_words
            successor_frequency = sum(cw.values())
            #Then find the probabilities of a word being the subsequent word. Then randomly draw one of these
            prob_of_being_succesor = list(map(lambda x: x/successor_frequency*100,cw.values()))
            sample_word = random.choices(list(cw.items()), weights = prob_of_being_succesor, k=1)
            
            cur_word = sample_word[0][0]
    return msg

def main():
     
     txt_file = sys.argv[1]
     start_word = sys.argv[2]
     max_nr_words = int(sys.argv[3])
    
     GeneratedShakespeare = text_generator(txt_file, start_word, max_nr_words)
     print("\n")
     print(GeneratedShakespeare)

if __name__ == "__main__":
    main()
