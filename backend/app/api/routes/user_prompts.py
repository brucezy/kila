from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.schemas import PromptRequest, PromptResponse, ExecutionStatus
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/prompts", tags=["prompts"])


@router.post("/", response_model=PromptResponse, status_code=201)
async def create_prompt(
        request: PromptRequest,
        db: AsyncSession = Depends(get_db)
):
    """
    Create a new prompt and process it with AI model.
    Uses idempotency_key to prevent duplicate submissions.
    """
    try:
        # Check for existing prompt with same idempotency key
        stmt = select(PromptRecord).where(
            PromptRecord.idempotency_key == request.idempotency_key
        )
        result = await db.execute(stmt)
        existing_prompt = result.scalar_one_or_none()

        if existing_prompt:
            logger.info(f"Duplicate request detected for idempotency_key: {request.idempotency_key}")
            return PromptResponse(
                id=existing_prompt.id,
                prompt=existing_prompt.prompt,
                project_name=existing_prompt.project_name,
                user_id=existing_prompt.user_id,
                execution_status=ExecutionStatus(existing_prompt.execution_status),
                ai_response=existing_prompt.ai_response,
                idempotency_key=existing_prompt.idempotency_key,
                created_at=existing_prompt.created_at,
                is_duplicate=True
            )

        # Create new prompt record with pending status
        new_prompt = PromptRecord(
            prompt=request.prompt,
            project_name=request.project_name,
            user_id=request.user_id,
            idempotency_key=request.idempotency_key,
            execution_status="pending"
        )

        db.add(new_prompt)
        await db.flush()  # Get the ID without committing

        # Process with AI model
        try:
            ai_response = await process_prompt(request.prompt)
            new_prompt.ai_response = ai_response
            new_prompt.execution_status = "success"
            logger.info(f"Successfully processed prompt ID: {new_prompt.id}")
        except Exception as ai_error:
            logger.error(f"AI processing failed for prompt ID {new_prompt.id}: {str(ai_error)}")
            new_prompt.execution_status = "failed"
            new_prompt.ai_response = f"Error: {str(ai_error)}"

        await db.commit()
        await db.refresh(new_prompt)

        return PromptResponse(
            id=new_prompt.id,
            prompt=new_prompt.prompt,
            project_name=new_prompt.project_name,
            user_id=new_prompt.user_id,
            execution_status=ExecutionStatus(new_prompt.execution_status),
            ai_response=new_prompt.ai_response,
            idempotency_key=new_prompt.idempotency_key,
            created_at=new_prompt.created_at,
            is_duplicate=False
        )

    except IntegrityError as e:
        await db.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=409,
            detail="Prompt with this idempotency key already exists"
        )
    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error creating prompt: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(
        prompt_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Retrieve a specific prompt by ID"""
    stmt = select(PromptRecord).where(PromptRecord.id == prompt_id)
    result = await db.execute(stmt)
    prompt = result.scalar_one_or_none()

    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    return PromptResponse(
        id=prompt.id,
        prompt=prompt.prompt,
        project_name=prompt.project_name,
        user_id=prompt.user_id,
        execution_status=ExecutionStatus(prompt.execution_status),
        ai_response=prompt.ai_response,
        idempotency_key=prompt.idempotency_key,
        created_at=prompt.created_at
    )

