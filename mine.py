"""
Having a look at the arxiv JSON file

2020-11
"""
import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import json
import re
from datetime import datetime
from tqdm import tqdm

def get_data():
    with open("arxiv-metadata-oai-snapshot.json") as fi:
        for li in fi:
            yield li

if __name__ == "__main__":
    docs = get_data()
    catr = re.compile(r'astro-ph\S*')
    mlr = re.compile(r'machine learning', re.IGNORECASE)
    mlr_ = re.compile(r'ML')
    dlr = re.compile(r'deep learning', re.IGNORECASE)
    nnr = re.compile(r'neural network', re.IGNORECASE)
    air = re.compile(r'artificial intelligence', re.IGNORECASE)
    air_ = re.compile(r'AI')
    #mlr = re.compile(r'maximum likelihood', re.IGNORECASE)
    #ganr = re.compile(r'GAN', re.IGNORECASE)
    ml = []
    dl = []
    nn = []
    ai = []
    astroph = []
    #gan = []

    for i, doc in tqdm(enumerate(docs), total=1789907):
        dat = json.loads(doc)
        date = dat["versions"][0]["created"]
        cats = dat["categories"].split()
        words = dat["abstract"].split()
        title = dat["title"].split()
        if any(catr.match(cat) for cat in cats):
            date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            astroph.append(date_.year + date_.month/12)
            if (any(air.match("{} {}".format(w1, w2)) for w1, w2 in zip(words, words[1:])) or
                    any(air.match("{} {}".format(w1, w2)) for w1, w2 in zip(title, title[1:])) or
                    any(air_.match(w1) for w1 in words) or any(air_.match(w1) for w1 in title)):
                date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                ai.append(date_.year + date_.month/12)
            if (any(mlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(words, words[1:])) or
                    any(mlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(title, title[1:])) or
                    any(mlr_.match(w1) for w1 in words) or any(mlr_.match(w1) for w1 in title)):
                date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                ml.append(date_.year + date_.month/12)
            if (any(dlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(words, words[1:])) or
                    any(dlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(title, title[1:]))):
                date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                dl.append(date_.year + date_.month/12)
            if (any(nnr.match("{} {}".format(w1, w2)) for w1, w2 in zip(words, words[1:])) or
                    any(nnr.match("{} {}".format(w1, w2)) for w1, w2 in zip(title, title[1:]))):
                date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
                nn.append(date_.year + date_.month/12)
            #if (any(ganr.match("{}".format(w1)) for w1 in words) or
            #        any(ganr.match("{}".format(w1)) for w1 in title)):
            #    date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            #    gan.append(date_.year + date_.month/12)
            #if (any(mlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(words, words[1:])) or
            #        any(mlr.match("{} {}".format(w1, w2)) for w1, w2 in zip(title, title[1:]))):
            #    date_ = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            #    ml.append(date_.year + date_.month/12)

    np.save("ai.npy", ai)
    np.save("ml.npy", ml)
    np.save("dl.npy", dl)
    np.save("nn.npy", nn)
    np.save("astroph.npy", astroph)

    exit()
    hml = np.histogram(ml, 100)
    plt.plot(hml[1][:-1], hml[0], label="ml")
    hdl = np.histogram(dl, 100)
    plt.plot(hdl[1][:-1], hdl[0], label="dl")
    hnn = np.histogram(nn, 100)
    plt.plot(hnn[1][:-1], hnn[0], label="nn")
    #hgan = np.histogram(gan, 100)
    #plt.plot(hgan[1][:-1], hgan[0], label="gan")
    plt.legend()
    plt.savefig("plots_.png")
