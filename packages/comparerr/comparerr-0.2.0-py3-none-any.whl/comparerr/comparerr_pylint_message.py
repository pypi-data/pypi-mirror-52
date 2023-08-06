class ComparerrMessage:
    def __init__(self, original_message, context):
        self.original_message = original_message
        self.context = context

    def display_message(self):
        print("Message: %s" % self.original_message.msg)
        print("Line: %s" % self.original_message.line)
        print("Context: \n%s" % self.context)
