#!/usr/bin/env python3

import unicodedata as uni
from collections import Counter
import numpy as np
import os
import sys



def validation():
    
    if len(sys.argv) < 2:
        print("Error! No input was given!")
        return False
    
    elif len(sys.argv) >=2:
        
        if sys.argv[1].endswith('.txt') is False:
            print("Error! Needs to be a .txt file!")
            return False
        
        elif os.path.isfile(sys.argv[0]) is False:
            print("Error! File does not exist.")
            return False
        
        else:
            return True


def file_input(file): 
    
    txt = open(file, 'r', encoding='utf-8')
    text_str = txt.read()
    
    text_str = uni.normalize('NFKD', text_str)
    text_str = text_str.lower()

    return text_str



def clean_data(txt_file):
    
    clean_txt = txt_file
    
    list_of_cleaned_letters = []
    for i in clean_txt:
        category = uni.category(i)
        if category in {"Ll", "Po"}:
            if i == "æ":
                list_of_cleaned_letters.append('a')
            else:    
                list_of_cleaned_letters.append(i)
        else:
            list_of_cleaned_letters.append(' ')
    
    cleaned_string = "".join(str(i) for i in list_of_cleaned_letters)
    
    return cleaned_string


def counting(filterd_txt, count_all_words=False, count_unique_words = False):
    
    cleaned_data = filterd_txt
    
    if count_all_words is True:
        NWords = len(cleaned_data.split())
        return NWords
    
    elif count_unique_words is True:
       return len(np.unique([cleaned_data.split()]))
    
    else:
        Freq_dict = {}
        for i in set(cleaned_data):
            if i.isalpha():
                Freq_dict[i] = cleaned_data.count(i)
        return sorted(Freq_dict.items(), key= lambda item: (-item[1]) )
    
    
def top_five(filterd_txt):
    
    frequency = Counter(filterd_txt.split())
    words_with_highest_freq = frequency.most_common(5)
    
    return words_with_highest_freq
    
def subsequent_words(filtered_txt, target_words, all_the_words = False):
    
    # If we want all the subsequent words, and their frequency, all_the_words are set to True. This flag is used in generate_txt.
    
    if all_the_words is True:
    
        AllUniqueWords = np.unique([filtered_txt.split()])
        UniqueDict = dict.fromkeys(AllUniqueWords)
    
        ArrayAllWords = np.array(filtered_txt.split())
    
        # Looping over all words in the txt, and getting each proceeding word. Then checking if that next word is None 
        # (i.e. has no proceeding values) we create a sub dictionary and then increment it each time it occurs as next word.
    
    
        for i, word in enumerate(ArrayAllWords[:len(ArrayAllWords) - 1]):
       
            NW = ArrayAllWords[i + 1]
            SubDict = UniqueDict[word]
           
            if SubDict is None:
                SubDict = {}
            if NW in SubDict:
                SubDict[NW] = SubDict[NW] + 1
            else:
                SubDict[NW] = 1
    
            UniqueDict[word] = SubDict
        
        return UniqueDict
    
    # Otherwise, if we only want the top three most common following words and their frequency 
    
    else:
        
        filtered_array = np.array(filtered_txt.split())
    
        all_the_following_words = [filtered_array[i + 1] for i, word in enumerate(filtered_array) if word == target_words]
        frec_of_words = {i: all_the_following_words.count(i) for i in set(all_the_following_words)}
    
        sorted_words = sorted(frec_of_words.items(), key= lambda item: (-item[1]) )
        
        return sorted_words[:3]   
    
    
    
def main():
    
   if validation() is True:
       
       text_file = sys.argv[1]
       validated_txt = file_input(text_file)
       processed_txt = clean_data(validated_txt)

       letter_frequency = counting(processed_txt)
       tot_words = counting(processed_txt, True)
       all_unique_words = counting(processed_txt, False, True)
    
       five_mc_words = top_five(processed_txt)
       
       # Looping over the five_mc_words, which is a list of 5 tuples (i.e. the 5 most common words and their frequency), as target_words 
       # in the function subsequent_words, to find the three most common subsequent words and their frequency.
       
       list_of_ss_words = [subsequent_words(processed_txt, five_mc_words[i][0]) for i in range(5)]    
    
       if len(sys.argv) > 2:
            OutputText = sys.argv[2]
            with open(OutputText,'w+') as f:
                f.write("Frequency Table for Alphabetic Letters:")
                f.write("\n")
                f.write('\n'.join('%s: %s' % x for x in letter_frequency))
                f.write("\n")
                f.write("\n")
                f.write("Total number of words in the text file: {}".format(tot_words))
                f.write("\n")
                f.write("Total number of unique words in the text file: {}".format(all_unique_words))
                f.write("\n")
                f.write("\n")
                f.write("The top five number of words, together with their most common subsequent words are:")
                f.write("\n")
                for i in range(5):
                    f.write("{} ({} occurrences)".format(five_mc_words[i][0], five_mc_words[i][1]))
                    f.write("\n")
                    for j in range(3):
                        inner_list = list_of_ss_words[i]
                        f.write("-- {}, {}".format(inner_list[j][0], inner_list[j][1]))
                        f.write("\n")
                    f.write("\n")
                
       else:
             print("\n")
             print("Frequency Table for Alphabetic Letters:")
             print("\n")
             for i in letter_frequency:
                     print(i, "\n")
             print("\n")
             print("Total number of words in the text file:", tot_words, "\n")
             print("Total number of unique words in the text file:", all_unique_words)
             print("\n")
             print("The top five number of words, together with their most common subsequent words are:")
             print("\n")
             for i in range(5):    
                 print("{} ({} occurrences)".format(five_mc_words[i][0], five_mc_words[i][1]), "\n")
                 inner_list = list_of_ss_words[i]
                 for j in range(3):
                     print("-- {}, {}".format(inner_list[j][0], inner_list[j][1]))
                     
                 print("\n")
             
   else:
        raise Exception("Error in file input.")
    
if __name__ == "__main__":
    main()
