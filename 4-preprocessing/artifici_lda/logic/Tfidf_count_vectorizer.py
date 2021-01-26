from sklearn.feature_extraction.text import TfidfVectorizer as CV


class TfidfVectorizer(CV):

    def inverse_transform(self, X):
        """
        Note: this method overrides the original one to retain the order of the features passed as argument.

        Return a list of words for each document, keeping the order of the transformed words indexes.
        """
        self._check_vocabulary()

        all_undid = []  # Let's undo that.
        for doc in X:
            undid_doc = [self.get_feature_names()[i] for i in doc]
            all_undid.append(undid_doc)
        return all_undid
