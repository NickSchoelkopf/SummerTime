
from summ_eval.rouge_metric import RougeMetric
from .Metric import Metric

class rouge(Metric):
    def __init__(self):
        super().__init__('rouge')
        self.se_rouge = RougeMetric()

    def evaluate(self, model, data):
        predictions = model.summarize(data['article'])
        self.score_dict = self.se_rouge.evaluate_batch(predictions,
            data['highlights'])

    def get_dict(self, keys):
        return {key: self.score_dict[self.metric_name][key]
            for key in keys}
