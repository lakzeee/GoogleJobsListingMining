from nltk.corpus import stopwords
import constants as const


def stop_words():
    sw = set(stopwords.words('english'))
    sw.update(const.CUSTOM_WORDS)
    return sw


def split_by_stop_word(sentence):
    sw = stop_words()
    prog_name = set(const.NAMES)
    data = sentence.lower() \
        .replace(",", "") \
        .replace(".", "") \
        .replace("(", "") \
        .replace(")", "") \
        .replace("<div>", "")\
        .replace("<", "") \
        .replace(">", "") \
        .replace("/", " and ") \
        .replace("'s", "") \
        .replace("’s", "") \
        .split(" ")

    word = ""
    for d in data:
        if d not in sw:
            if d not in prog_name:
                word += d
                word += " "
            else:
                word += d
                word += ","
        else:
            word += ","
    word = word.split(",")
    word = [item.strip() for item in word if len(item) > 0]
    # print(word)
    return word

