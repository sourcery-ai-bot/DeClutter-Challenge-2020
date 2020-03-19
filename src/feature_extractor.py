import re
from sklearn.feature_extraction.text import TfidfVectorizer
from src.csv_utils import get_comments, get_tags, get_javadoc_comments
from src.code_parser import get_code_words, word_extractor, tokenizer
from src.keys import reports_outpath


def get_tfidf_features():
    comments = get_comments()
    tfidf_vector = TfidfVectorizer(tokenizer=tokenizer, lowercase=False)
    tfidf_vector.fit_transform(comments)
    file = open(reports_outpath+"tfidf_features.txt", 'w')
    for key in tfidf_vector.vocabulary_.keys():
        file.write(key)
        file.write("\n")
    return tfidf_vector.vocabulary_


def get_tag_for_comment():
    return get_tag_for_list(get_comments())


def get_tag_for_list(comments):
    tags_dict = {}
    for i in range(len(comments)):
        tags_dict[i] = []

    tags = get_tags()
    for tag in tags:
        i = 0
        for comment in comments:
            if re.search(tag, comment):
                tags_dict[i].append(tag)
            i += 1
    return tags_dict


def get_comment_words(stemming=True, rem_keyws=True):
    comments = get_comments()
    words = []
    for comment in comments:
        words.append(word_extractor(comment, stemming, rem_keyws))
    return words


def jaccard(stemming=True, rem_keyws=True):
    code = get_code_words(stemming, rem_keyws)
    comments = get_comment_words(stemming, rem_keyws)
    score = []
    for i in range(len(comments)):
        score.append(get_jaccard_sim(code[i], comments[i]))
    return score


def get_jaccard_sim(first, second):
    a = set(first)
    b = set(second)
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def get_comment_length():
    comments = get_comments()
    return [len(comment) for comment in comments]


def get_javadoc_tags():
    return get_tag_for_list(get_javadoc_comments())


if __name__ == '__main__':
    #jaccard()
    #print(get_javadoc_tags())
    print(get_tfidf_features())