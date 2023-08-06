from collections import Counter
from wordcloud.wordcloud import WordCloud
from matplotlib import pyplot as plt
## Common Data Util methods
        
def plotword_cloud(word_dict, figsz=(10,5)):
    """
    Plot wordcloud:
    Inputs: filename | list | frequency_dict
    """
    if isinstance(word_dict, dict):
        pass
    elif isinstance(word_dict, list):
        word_dict = Counter(word_dict)
    elif isinstance(word_dict, str):
        fname = word_dict
        with open(fname) as f:
            data = f.read().split()
            word_dict = Counter(data)
    else:
        raise Exception("expected dict")
    wc = WordCloud()
    wc_img = wc.generate_from_frequencies(word_dict)
    plt.figure(figsize=figsz)
    plt.imshow(wc_img, interpolation="bilinear")
    plt.axis('off')
    plt.show()