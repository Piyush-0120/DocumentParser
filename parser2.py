'''This parser fixes the adverbs and find synonyms for words'''
import os.path
import nltk
from nltk.corpus import wordnet
from nltk.tag.senna import SennaTagger
from parser1_v2 import Parser

class Parser2(Parser):
    
    def adv_to_adj(self,word):
        s = []
        nearest_word = ""
        #print(wordnet.synsets(word))
        for ss in wordnet.synsets(word):
            for lemmas in ss.lemmas(): # all possible lemmas.
                s.append(lemmas)

        for pers in s:
            if len(pers.pertainyms())==0: continue
            posword = pers.pertainyms()[0].name()
            if posword[0:3] == word[0:3]:
                nearest_word = posword
                break
        if nearest_word !="":
            return nearest_word
        return word
    
    def fix_adverbs(self): #  ************(call this)
        lemmatized_words = self.get_lemmatized_words()
        important_words = self.important_words        #(word,tag)
        fix =[]
        for i in range(len(important_words)):
            if(important_words[i][1][0]=="R"):
                fix.append(self.adv_to_adj(important_words[i][0]))
            else:
                fix.append(lemmatized_words[i])
        print(fix)


document1 = """Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
The sky is pinkish-blue. You shouldn't eat cardboard. I loved studying but now I do coding, crying"""
document2= """Long ago, when there was no written history, these islands were the home of millions of happy birds; the resort of a hundred times more millions of fishes, sea lions, and other creatures.
Here lived innumerable creatures predestined from the creation of the world to lay up a store of wealth for the British farmer, and a store of quite another sort for an immaculate Republican government."""
document3= """In ages which have no record these islands were the home of millions of happy birds, the resort of a hundred times more millions of fishes, of sea lions,
and other creatures whose names are not so common; the marine residence, in fact, of innumerable creatures predestined from the creation of the world to lay up a store of wealth for the British farmer,
and a store of quite another sort for an immaculate Republican government."""
document4="""Only two years later, all these friendly Sioux were suddenly plunged into new conditions, including starvation, martial law on all their reservations, and constant urging by their friends and relations to join in warfare against the treacherous government that had kept faith with neither friend nor foe."""
document5="""In ages which have no record these islands were the home of millions of "Contrast the condition into which all these friendly Indians are suddenly plunged now, with their condition only two years previous: martial law now in force on all their reservations; themselves in danger of starvation, and constantly exposed to the influence of emissaries from their friends and relations, urging them to join in fighting this treacherous government that had kept faith with nobody--neither with friend nor with foe."""
document6="The quick brown fox is jumping over the lazy dog so quickly"

p=Parser2(document6)
p.fix_adverbs()
