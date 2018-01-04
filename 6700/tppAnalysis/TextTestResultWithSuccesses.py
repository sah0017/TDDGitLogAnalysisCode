from unittest import TextTestResult


class TextTestResultWithSucesses(TextTestResult):
    def __init__(self, *args, **kwargs):
        super(TextTestResultWithSucesses, self).__init__(*args, **kwargs)
        self.successes = []
    def addSuccess(self, test):
        super(TextTestResultWithSucesses, self).addSuccess(test)
        self.successes.append(test)

