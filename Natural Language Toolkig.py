from nltk.tokenize import word_tokenize
from nltk import regexp_tokenize
from lxml import etree
from collections import defaultdict
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

class MostFreq:
    def __init__(self,):
        self.header = ""
        self.lemmatizer = WordNetLemmatizer()
        self.all_news = []

    def get_tokens(self, root):
        for element in root.iter('value'):
            if element.get('name') == 'head':
                self.status = f'{element.text}'
            elif element.get('name') == 'text':
                self.lemmatization(word_tokenize(element.text.lower()))

    #     for j in range(len(root[0])):
    #         for i in range(len(root[0][0])):
    #             if i % 2 == 0:
    #                 self.status = f'{root[0][j][i].text}:'
    #             else:
    #                 # self.all_news.append(root[0][j][i].text.lower())
    #                 self.lemmatization(word_tokenize(root[0][j][i].text.lower()))
    # #HOW TO PARSE XML AND FIND TEXT FOR TAG WITH PARTICULAR ATTRIBUTE

    def all_news_2_list(self, root):
        for element in root.iter('value'):
            if element.get('name') == 'text':
                self.all_news.append(' '.join(element.text.split()))
                # self.all_news.append((element.text))

    def metrics(self, NN_only):
        new_ = []
        for el in NN_only:
            if el not in new_:
                new_.append(el)
        my_vocab = (sorted(list(set(NN_only))))
        vectorizer = TfidfVectorizer(vocabulary=my_vocab)
        dataset = self.all_news
        self.tfidf_matrix = vectorizer.fit_transform(dataset)
        terms = vectorizer.get_feature_names()
        feature_index = self.tfidf_matrix.nonzero()[1]
        index_2_word = [terms[x] for x in feature_index]
        # print(list(zip(feature_index, index_2_word)))
        # print(vectorizer.vocabulary_.items())
        # print(sorted(words_from_index))
        tfidf_scores = zip(index_2_word, [self.tfidf_matrix[y, x] for x in feature_index for y in range(len(dataset))])

        # print(sorted(vectorizer.vocabulary_.items()))
        # print(list(tfidf_scores))
        # print(list(tfidf_scores))
        sorted_tfidf_scores = sorted(list(tfidf_scores), key=lambda x: x[1], reverse=True)
        print(sorted_tfidf_scores)
        # print('xxxxxxxxxxxxxxxxxxxxxxxxxx')
        # most_common_terms = [terms[sorted_tfidf_scores[i][0]] for i in range(10)]
        # print(most_common_terms)

    def lemmatization(self, tokens):
        self.lemmatized = [self.lemmatizer.lemmatize(el) for el in tokens]
        wihtout_punct = [token for token in self.lemmatized if token not in list(string.punctuation)]
        without_stopwords = [el for el in wihtout_punct if el not in stopwords.words('english')]
        self.pos_tagging(without_stopwords)

    def pos_tagging(self, list_of_words):
        word_n_tag = [nltk.pos_tag([el])[0] for el in list_of_words]
        NN_only = [el[0] for el in word_n_tag if el[1] == 'NN']
        # print(NN_only)
        self.metrics(NN_only)
        # self.count_the_words(NN_only)

    def count_the_words(self, tokens):
        self.freq_defaultdict = defaultdict(int)
        self.words = []
        for word in tokens:
            self.freq_defaultdict[word] += 1
        sorted_dict = sorted(self.freq_defaultdict.items(), key=lambda i: (i[1], i[0]), reverse=True)
        counter = Counter(sorted_dict)
        for el in counter.most_common(5):
            self.words.append(el[0][0])
        self.print_result()

    def print_result(self):
        print()
        print(self.status)
        print(" ".join(self.words))



def main():
    xml_file = "news.xml"
    root = etree.parse(xml_file)
    tokenize = MostFreq()
    tokenize.all_news_2_list(root)
    tokenize.get_tokens(root)
    print(tokenize.tfidf_matrix)
main()
