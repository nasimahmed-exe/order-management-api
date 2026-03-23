from typing import TypeVar,Type,Generic
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType,CreateSchemaType]):
    def __init__(self,model : Type[ModelType]):
        self.model = model

    def create(self, db: Session, *, obj_in:CreateSchemaType)->ModelType:

        model_name = self.model.__name__
        logger.info(f"CRUDBase: Initiating [CREATE] for model: {model_name}")
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)

        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            # Log the success and the new ID
            logger.info(f"CRUDBase: Successfully saved {model_name} with ID: {db_obj.id}")
            return db_obj
        except Exception as e:
            logger.error(f"CRUDBase: Failed to create {model_name}. Error: {str(e)}")
            db.rollback()
            raise e

        
        





