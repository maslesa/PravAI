from fastapi import APIRouter, Depends, HTTPException
from ..dependecies import get_query_service
from ..schemas.query import CitationResponse, QueryRequest, QueryResponse
from ..services.query_service import QueryService
from fastapi.responses import StreamingResponse


router = APIRouter(
    prefix="/query",
    tags=["Query"],
)

@router.post('', response_model=QueryResponse)
def query(request: QueryRequest, service: QueryService = Depends(get_query_service)) -> QueryResponse:
    try:
        result = service.answer_question(question=request.question)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error

    citations = [CitationResponse(law=citation.law, article=citation.article) for citation in result.citations] if result.citations else []

    return QueryResponse(
        answer=result.answer,
        citations=citations,
        grounded=result.grounded,
    )


@router.post('/stream', response_class=StreamingResponse)
def stream_query(request: QueryRequest, service: QueryService = Depends(get_query_service)):
    return StreamingResponse(
        service.stream_answer(question=request.question),
        media_type='application/x-ndjson',
        headers={
            'Cache-Control': 'no-cache',
            'X_Accel-Buffering': 'no',
        }
    )