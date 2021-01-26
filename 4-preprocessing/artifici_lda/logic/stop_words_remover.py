import os
import string

from sklearn.base import BaseEstimator, TransformerMixin
import translitcodec

STOPWORDS_FILENAME = "custom_FR_EN_stop_words.txt"


class StopWordsRemover(BaseEstimator, TransformerMixin):
    def __init__(self, stopwords=None):
        """
        This stop word remover is built so as to be very gentle with the
        input strings so as to keep their structure as much as possible.

        If no stopwords are passed, it will try to load them from disks at the path of `STOPWORDS_FILENAME`.
        """
        self.stopwords = stopwords
        self.safe_stopwords = None

    def get_params(self, deep=True):
        """
        This function is implemented for the class to be usable by scikit-learn's Pipeline() behavior.
        """
        return dict()

    def set_params(self, **parameters):
        """
        This function is implemented for the class to be usable by scikit-learn's Pipeline() behavior.
        """
        for parameter, value in parameters.items():
            self.__setattr__(parameter, value)
        return self

    def fit(self, X=None, y=None):
        """
        This function is implemented for the class to be usable by scikit-learn's Pipeline() behavior.
        X & y are ignored here, but required by convention.

        It reads the stopwords from disk if there are none provided.
        """

        if self.stopwords is None:
            current_dir = os.path.dirname(os.path.realpath(__file__))
            stop_words_file = os.path.join(current_dir, "..", "data", STOPWORDS_FILENAME)
            with open(stop_words_file) as f:
                self.stopwords = f.read().split("\n")
        self.safe_stopwords = [translitcodec.long_encode(w)[0].lower() for w in self.stopwords]

        return self

    def transform(self, text):
        """
        This function is implemented for the class to be usable by scikit-learn's Pipeline() behavior.

        This function only recurse and then call the single "self.remove_from_string(...)".
        This means that this version is a vectorized version of "self.remove_from_string(...)"
        """
        if self.safe_stopwords is None:
            self.fit()

        if isinstance(text, str):
            return self.remove_from_string(text)

        else:
            # It should be an iterable, recurse to find text at a lower branch deep down.
            ret_list = []
            for inner in text:
                inner = self.transform(inner)
                ret_list.append(inner)
            return ret_list

    def remove_from_string(self, text):
        """
        Remove stopwords from a string in the safest possible way to keep the text intact.
        """

        # In the following variables, text's characters will flow from bottom to top such as:
        # text --> last_word|last_punct --> past_text
        past_text = ""
        last_punct = ""
        last_word = ""

        text += "."  # add a last punctuation to loop 1 last time closing the sentence.
        for char in text:
            decoded_char = translitcodec.short_encode(char)[0].lower()

            char_is_letter = False
            if decoded_char in string.ascii_lowercase:  # Lowercase alphabet
                char_is_letter = True

            # We loop if it's part of a word.
            if char_is_letter:
                # We're building a word.
                # Loop
                last_word += char

            # Otherwise if it's punctuation, we're either somehow before or directly after a word.
            elif not char_is_letter:

                # We ignore N punctuations in a row before a word.
                if last_word == "":
                    # Move on.
                    last_punct += char
                # Otherwise we're closing a word. Let's process it now.
                else:
                    full_word = last_word
                    safe_full_word = translitcodec.long_encode(full_word)[0].lower()
                    if safe_full_word in self.safe_stopwords:
                        # We remove the word (and the following apostrophe or space if there is one)!
                        full_word = ""
                        if char in "’'‘’'' ":
                            char = ""

                    # Loop
                    past_text += last_punct + full_word
                    last_punct = char
                    last_word = ""

        past_text += last_punct
        return past_text[:-1]

    def inverse_transform(self, text):
        return text
