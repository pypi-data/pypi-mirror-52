from pylint.reporters import BaseReporter

class ComparerrReporter(BaseReporter):
    def __init__(self):
        super().__init__()
        self.errors = []

    def handle_message(self, msg):
        self.errors.append(msg)
