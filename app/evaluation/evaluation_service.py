from datasets import Dataset

from app.evaluation.ragas_evaluator import (
    RAGASEvaluator,
)



class EvaluationService:


    def __init__(self):

        self.evaluator = RAGASEvaluator()



    async def run(

        self,

        records:list[dict],

    ):


        dataset = Dataset.from_dict(

            {

                "question":

                [

                    r["question"]

                    for r in records

                ],


                "answer":

                [

                    r["answer"]

                    for r in records

                ],


                "contexts":

                [

                    r["contexts"]

                    for r in records

                ],


                "ground_truth":

                [

                    r["ground_truth"]

                    for r in records

                ],

            }

        )


        result = await self.evaluator.evaluate(

            dataset

        )


        return result