"""
This parser fixes the adverbs.
    Output for parser1_v2
    >>>['quick', 'brown', 'fox', 'jump', 'lazy', 'dog', 'quickly']
        Adverb quickly remains same it didn't changed to quick.
"""
from nltk.corpus import wordnet
from parser1_v2 import Parser

class Parser2(Parser):
    
    def adv_to_adj(self,word):
        """
        This method changes adverbs to adjectives.
        In simple words, it finds the nearest base word of any adverb.
        If it does not find, then returns the same word.
        """
        s = []
        nearest_word = ""
        try:
            for ss in wordnet.synsets(word):
                for lemmas in ss.lemmas():      # all possible lemmas.
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
        except Exception as e:
            print(e)
    
    def parsed_words(self):
        """
        It fixes the adverbs of self.important_words.
        Attribute self.important_words is also an attribute of Parser2 as it inherits Parser1.
        Attribute self.important_words is a list of tuples(word,tag)
        This method returns the final parsed words of the document
        """
        try:
            lemmatized_words = self.get_lemmatized_words()
            important_words = self.important_words
     
            final_parsed_words =[]
            for i in range(len(important_words)):
                if(important_words[i][1][0]=="R"):
                    final_parsed_words.append(self.adv_to_adj(important_words[i][0]))
                else:
                    final_parsed_words.append(lemmatized_words[i])
            return final_parsed_words
        except Exception as e:
            print(e)



if __name__=="__main__":
    # Sample document
    document= """Long ago, when there was no written history, these islands were the home of millions of happy birds; the resort of a hundred times more millions of fishes, sea lions, and other creatures.
    Here lived innumerable creatures predestined from the creation of the world to lay up a store of wealth for the British farmer, and a store of quite another sort for an immaculate Republican government."""
    p=Parser2(document)
    print(p.parsed_words())
