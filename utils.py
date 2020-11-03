import numpy as np, numpy.random

class utils():
    def __init__(self):
        pass


    def calculate_fake_news_score(url):
        # get the random 4 values that summed to one
        score = np.random.dirichlet(np.ones(4), size=1)
        print(score, flush=True)
        stance = "agree"
        return score
