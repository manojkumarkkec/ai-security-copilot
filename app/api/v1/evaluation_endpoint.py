from fastapi import APIRouter


from app.evaluation.evaluation_service import (
    EvaluationService,
)


from app.evaluation.evaluation_dataset import (
    EVALUATION_DATA,
)



router = APIRouter(

    prefix="/evaluation",

    tags=["Evaluation"]

)



service = EvaluationService()



@router.post("/run")
async def run_evaluation():


    result = await service.run(

        EVALUATION_DATA

    )


    return {


        "metrics":

        result,

    }