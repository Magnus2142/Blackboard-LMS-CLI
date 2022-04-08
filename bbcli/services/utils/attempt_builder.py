class AttemptBuilder(object):
    def __init__(self, status=None, score=None, text=None, notes=None, feedback=None, studentComments=None, studentSubmission=None, exempt=None) -> None:
        self.status = status
        self.score = score
        self.text = text
        self.notes = notes
        self.feedback = feedback
        self.studentComments = studentComments
        self.studentSubmission = studentSubmission
        self.exempt = exempt

    def create_json(self):
        attempt = {}
        if self.status:
            attempt.update({
                'status': self.status
            })
        if self.score:
            attempt.update({
                'score': self.score
            })
        if self.text:
            attempt.update({
                'text': self.text
            })
        if self.notes:
            attempt.update({
                'notes': self.notes
            })
        if self.feedback:
            attempt.update({
                'feedback': self.feedback
            })
        if self.studentComments:
            attempt.update({
                'studentComments': self.studentComments
            })
        if self.studentSubmission:
            attempt.update({
                'studentSubmission': self.studentSubmission
            })
        if self.exempt:
            attempt.update({
                'exempt': self.exempt
            })
        return attempt
