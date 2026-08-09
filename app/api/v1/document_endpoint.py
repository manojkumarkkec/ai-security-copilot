from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
)


from sqlalchemy.ext.asyncio import AsyncSession


from app.database.session import get_db


from app.services.document_ingestion_service import (
    DocumentIngestionService,
)



router = APIRouter(

    prefix="/documents",

    tags=["Documents"]

)



@router.post("/upload")
async def upload_document(

    file: UploadFile = File(...),

    db: AsyncSession = Depends(get_db),

):


    content = await file.read()


    service = DocumentIngestionService()


    result = await service.ingest(

        session=db,

        filename=file.filename,

        content=content,

    )


    return {


        "message": "Document indexed successfully",

        **result

    }