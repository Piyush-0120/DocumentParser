import os.path
import re
import nltk
from nltk.corpus import wordnet
from nltk.tag.senna import SennaTagger

class Parser:
    def __init__(self, document):
        self.document = document
        self.sentences =None
        self.words=None
        self.tag_dict=None
        self.important_words=None
        self.lemmatized_word=None

    def tokenize_sentence(self):
        """
        Used to tokenize the paragraphs into sentences.
        This method will return the sentences after removing all the punctuators
        """
        try:
            tokenized_sentence=nltk.tokenize.sent_tokenize(self.document)
        except Exception as e:
            print(e.__class__, "occurred.")
            print("punkt was not downloaded!")
            print("type nltk.download('punkt') in python shell")
        sentences=[]
        for sentence in tokenized_sentence:
            punctuation = re.compile(r'[-.?!,:;()\"|0-9]')
            s = punctuation.sub(' ',sentence)    #any further punctuators or separators do it in tokenize_word()
            sentences.append(s)
        self.sentences = sentences
        #print(sentences,end="\n")

    def tokenize_word(self):
        """
        This method tokenizes the sentences into words.
        The original words can be used for locating in document
        """
        words = []                     
        for sentence in self.sentences:
            words.extend(sentence.split())      #any further removal of punctuators or separators do it in here
        self.words = words 
        #print(words,end="\n")

    def get_senna_tags_sentences(self):
        """
        Assigns the part of speech to word of a sentence using SennaTagger.
        To use the SennaTagger, you need to download the zip file.
        Here, "\Downloads\senna-v3.0\senna" is the default location of senna.exe
        after unzipping the file in Downloads folder.
        """
        try:
            home = os.path.expanduser('~')
            st = SennaTagger(home+"\Downloads\senna-v3.0\senna")
            tag_dict =[] 
            for sentence in self.sentences:
                try:
                    tag_dict.extend((st.tag(sentence.split())))
                except Exception as e:
                    print(e.__class__, "occurred.")
                    print("type nltk.download('tagsets') in python shell")

            self.tag_dict=tag_dict

        except Exception as e:
            print(e.__class__, "occurred.")
            print("senna.exe was not found at that path!")
        #print(tag_dict,end="\n")

    def remove_common_words(self):
        """
        This method removes the common words like is,am,are,etc.
        Attribute self.tag_dict is list of tuple(word,tag)
        """
        try:
            important_words=[]
            common_words=set(nltk.corpus.stopwords.words("english"))
            for word in self.tag_dict:
                if word[0].lower() not in common_words:
                    important_words.append(word)          
            self.important_words = important_words
        except Exception as e:
            print(e.__class__, "occurred.")
            print("stopwords was not downloaded!")
            print("type nltk.download('stopwords') in python shell")

        #print(important_words,end="\n")
               
    def get_wordnet_pos(self,word):
        """
        IF you don't want to download SennaTagger then you can use this method to
        assign part of speech and maps the wordnet tag used by the lemmatizer function below.
        Parameter word is a string
        """
        try:
            tag = nltk.pos_tag([word])[0][1][0].upper()
        except Exception as e:
            print(e.__class__, "occurred.")
            print("type nltk.download('tagsets') in python shell")
        try:
            tag_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return tag_dict.get(tag, wordnet.NOUN)
        except Exception as e:
            print(e.__class__, "occurred.")
            print("type nltk.download('wordnet') in python shell")

    def get_senna_pos(self,word):
        '''
        This method will return for each word a wordnet tag used by the lemmatizer function below
        Parameter word is a tuple(word,tag)
        '''
        try:
            tag=word[1][0].upper()
            t_dict = {"J": wordnet.ADJ,
                        "N": wordnet.NOUN,
                        "V": wordnet.VERB,
                        "R": wordnet.ADV}
            return t_dict.get(tag, wordnet.NOUN)
        except Exception as e:
            print(e.__class__, "occurred.")
            print("type nltk.download('wordnet') in python shell")            


    def lemmatization_with_pos_tags(self):
        """
        This method is used to lemmatize words to their base words.
        For example, loved -> love, raining -> rain
        Attribute self.important_words is a list of tuples(word,tag)
        """
        try:
            lem = nltk.stem.wordnet.WordNetLemmatizer()
            lemmatized_words=[]
            for word in self.important_words:
                tag = self.get_senna_pos(word)
                lemmatized_word = lem.lemmatize(word[0],tag)
                lemmatized_words.append(lemmatized_word.lower())
            self.lemmatized_word=lemmatized_words
        except:
            print("error in nltk.stem.wordnet.WordNetLemmatizer()")

    
    def get_lemmatized_words(self):
        """
        Driver method to get the lemmatized words
        This method assigns all the attributes of the Parser class with the corresponding values
        """
        self.tokenize_sentence()
        self.tokenize_word()
        self.get_senna_tags_sentences()
        self.remove_common_words()
        self.lemmatization_with_pos_tags()
        return self.lemmatized_word

if __name__=="__main__":
    '''
    Sample documents
    '''
    document1 = """Hello Mr. Smith, how are you doing today? The weather is great, and city is awesome.
    The sky is pinkish-blue and it is raining. You shouldn't eat cardboard. I loved studying but now I also love coding"""
    document2= """Long ago, when there was no written history, these islands were the home of millions of happy birds; the resort of a hundred times more millions of fishes, sea lions, and other creatures.
    Here lived innumerable creatures predestined from the creation of the world to lay up a store of wealth for the British farmer, and a store of quite another sort for an immaculate Republican government."""
    document3= """In ages which have no record these islands were the home of millions of happy birds, the resort of a hundred times more millions of fishes, of sea lions,
    and other creatures whose names are not so common; the marine residence, in fact, of innumerable creatures predestined from the creation of the world to lay up a store of wealth for the British farmer,
    and a store of quite another sort for an immaculate Republican government."""
    document4="""Only two years later, all these friendly Sioux were suddenly plunged into new conditions, including starvation, martial law on all their reservations, and constant urging by their friends and relations to join in warfare against the treacherous government that had kept faith with neither friend nor foe."""
    document5="""In ages which have no record these islands were the home of millions of "Contrast the condition into which all these friendly Indians are suddenly plunged now, with their condition only two years previous: martial law now in force on all their reservations; themselves in danger of starvation, and constantly exposed to the influence of emissaries from their friends and relations, urging them to join in fighting this treacherous government that had kept faith with nobody--neither with friend nor with foe."""
    document6="The quick brown fox is jumping over the lazy dog so quickly"
    
    p=Parser(document5)
    words = p.get_lemmatized_words()
    print(words)

