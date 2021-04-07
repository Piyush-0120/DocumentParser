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
        tokenized_sentence=nltk.tokenize.sent_tokenize(self.document)
        sentences=[]
        for sentence in tokenized_sentence:
            punctuation = re.compile(r'[-.?!,:;()|0-9]')
            s = punctuation.sub(' ',sentence)
            #any further punctuators or separators do it in words
            sentences.append(s)
        self.sentences = sentences
        #print(sentences,end="\n")

    def tokenize_word(self):
        '''
        sentences = self.sentences
        words=[]
        for sentence in sentences:
            #tokenized_word=nltk.tokenize.word_tokenize(sentence)
            tokenized_word = sentence.split()
            words.extend(tokenized_word)
        '''
        #any further punctuators or separators do it in here
        words = []
        for sentence in self.sentences:
            words.extend(sentence.split())
        # The original words can be used for locating in document
        #print(words,end="\n")
        self.words = words 

    def get_senna_tags_sentences(self):
        home = os.path.expanduser('~')
        # download SennaTagger and unzip it and provide the location to the senna-v3.0.exe
        st = SennaTagger(home+"\Downloads\senna-v3.0\senna")
        tag_dict =[] 
        for sentence in self.sentences:
            tag_dict.extend((st.tag(sentence.split())))
        self.tag_dict=tag_dict
        #print(tag_dict,end="\n")

    def remove_common_words(self):
        important_words=[]
        common_words=set(nltk.corpus.stopwords.words("english"))
        for word in self.tag_dict:
            if word[0].lower() not in common_words:
                important_words.append(word)           #word is a tuple
        self.important_words = important_words
        #print(important_words,end="\n")
               
    def get_wordnet_pos(self,word):
        #Map POS tag to first character lemmatize() accepts, word is string
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)
    
    def get_senna_pos(self,word):
        '''
        Applies the tag method over a list of sentences. This method will return for each sentence a list of tuples of (word, tag).
        parameter word is a tuple(word,TAG)
        '''
        tag=word[1][0].upper()
        t_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return t_dict.get(tag, wordnet.NOUN)


    def lemmatization_with_pos_tags(self):
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lemmatized_words=[]
        #self.important_words returns list of tuples
        for word in self.important_words:
            tag = self.get_senna_pos(word)
            lemmatized_word = lem.lemmatize(word[0],tag)
            lemmatized_words.append(lemmatized_word.lower())
        self.lemmatized_word=lemmatized_words

    
    def get_lemmatized_words(self):
        self.tokenize_sentence()
        self.tokenize_word()
        self.get_senna_tags_sentences()
        self.remove_common_words()
        self.lemmatization_with_pos_tags()
        return self.lemmatized_word

if __name__=="__main__":
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
    
    p=Parser(document6)
    p.tokenize_sentence()
    p.get_senna_tags_sentences()
    p.tokenize_word()
    p.remove_common_words()
    p.lemmatization_with_pos_tags()
    print(p.lemmatized_word)


'''
    home = os.path.expanduser('~')
    st = SennaTagger(home+"\Downloads\senna-v3.0\senna")
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    
    print("-------------SennaTagger-------------")
    tokenized_sentence=nltk.tokenize.sent_tokenize(p.document)
    for i in tokenized_sentence:
        print(st.tag(i.split()),end=" ")
    
    print("\n-------------SennaTagger with parsed sentences-------------")
    for i in p.sentences:
        print(st.tag(i.split()),end=" ")
    
    print("\n-------------SennaTagger with tokenized words-------------")
    w = []
    tokenized_word=nltk.tokenize.word_tokenize(p.document)
    common_words=set(nltk.corpus.stopwords.words("english"))
    
    #print(w,end="\n")
    punctuation = re.compile(r'[.?!,:;\'()|0-9]')
    post_punctuation=[]
    for words in tokenized_word:
        z=punctuation.sub('',words)
        if len(z)>2:
            post_punctuation.append(z)
    #print(post_punctuation)
    _tags=[]
    for i in post_punctuation:
        #print(st.tag([i]),end=" ")
        _tags.extend(st.tag([i]))
    print(_tags)

    for word in _tags:
        if word[0].lower() not in common_words:
            w.append(word)
    print(w,end="\n")
    lemmatized_words =[]
    
    for i in w:
        tag = p.get_senna_pos(i)
        lemmatizer = lem.lemmatize(i[0],tag)
        lemmatized_words.append(lemmatizer)
    print("\n---------------*************------------------\n")
    print(lemmatized_words)
    print("\nLemmetized words--->\n")
    print(p.lemmatized_word)

    print("\n-------------POSTagger-------------")    
    for i in tokenized_sentence:
        print(nltk.pos_tag(i.split()),end=" ")
    print()
    x="terribly"
    print(st.tag([x]))
    print(lem.lemmatize(x,'r'))
'''
