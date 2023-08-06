from analysis.handle import ArticleHandle


class PublicOpinionService:
    def __init__(self):
        self.handler = ArticleHandle()

    def _service(self):
        self.handler.update_topic(100)
        self.handler.update_sentiment(100)

    def update(self):
        self._service()