from ragas import evaluate
class RAGASEvaluator:

    def __init__(self):

        self.metrics = None


    async def evaluate(
            

        self,

        dataset,

    ):

        from ragas import evaluate

        from ragas.metrics import (

            faithfulness,

            answer_relevancy,

            context_precision,

            context_recall,

        )


        self.metrics = [

            faithfulness,

            answer_relevancy,

            context_precision,

            context_recall,

        ]


        result = evaluate(

            dataset,

            metrics=self.metrics,

        )


        return result