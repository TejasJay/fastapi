from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from model.models import Review
from schema import ReviewCreate


async def create_review(review_data: ReviewCreate, session: AsyncSession) -> Review:
    db_review = Review.model_validate(review_data)
    session.add(db_review)
    await session.commit()
    await session.refresh(db_review)
    return db_review

async def get_reviews_for_product(product_id: int, session: AsyncSession) -> List[Review]:
    """
    Retrieves all reviews for a specific product.
    """
    statement = select(Review).where(Review.product_id == product_id)
    result = await session.exec(statement)
    return result.all()   