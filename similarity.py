import re, math
from collections import Counter
import pandas as pd

WORD = re.compile(r'\w+')

sentenceList = [
    "پول نمیتونم بدم",
    "پرداخت مشکل داره آقا",
    "آقا این وجوهات شرعیمونو کجا بدیم",
    "پشه شبا کجا استاد میشه؟",
    "هر کسی بامش بیش پولش بیش",
    "باورم نمیشه شما هم خراب باشین واقعا ",
    "یک روز خوب میاد",
    "وای اگه این مالتی تب درست بشه چی میشه",
    "دلم گرفته از اپتون آخه",
    "وای چقدر مستم من",

]

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def get_top_similarity(sentence, bags, topCount):
    df = pd.DataFrame([])
    for i in range(len(bags)):
        print(bags[i])
        d = {'col1': [i], 'col2': [get_cosine(text_to_vector(sentence), text_to_vector(bags[i]))]}
        data = pd.DataFrame(data=d)
        df = df.append(data)

    df = df.sort_values(by=['col2'], ascending=False)
    print(df)
    result = []

    for i in range(min(topCount, len(bags))):
        if df['col2'].values[i] < 0.2:
            break
        result.append(bags[df['col1'].values[i]])
    return result

# text1 = 'خر ما خراب است'
# res = get_top_similarity(text1, sentenceList, 5)
# for i in range(len(res)):
#     print(res[i])

#print("Cosine:" + str(cosine))
