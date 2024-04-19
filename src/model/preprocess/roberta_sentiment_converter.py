import numpy as np

class RobertaSentimentConverter:
    def __init__(self) -> None:
        pass

    def sentiment_to_num(self, sentiment_arr: np.array)->np.array:
        numeric_sentiments = np.zeros_like(sentiment_arr, dtype=np.int32)
        for i, sentiment in enumerate(sentiment_arr):
            if sentiment == 'Negative':
                numeric_sentiments[i] = 0
            elif sentiment == 'Neutral':
                numeric_sentiments[i] = 1
            elif sentiment == 'Positive':
                numeric_sentiments[i] = 2
            else:
                raise ValueError("Invalid sentiment label")
        return numeric_sentiments
    
    def num_to_sentiment(self, number_arr: np.array) -> np.array:
        text_sentiments = np.zeros_like(number_arr, dtype=np.int32)
        for i, number in enumerate(number_arr):
            if number == 0:
                text_sentiments[i] = 'Negative'
            elif number == 1:
                text_sentiments[i] = 'Neutral'
            elif number == 2:
                text_sentiments[i] = 'Positive'
            else:
                raise ValueError("Invalid integer label")
        return text_sentiments
