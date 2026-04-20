from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body

from sqlalchemy.future import select 
from sqlalchemy.ext.asyncio import AsyncSession 
from app import models,schemas,utils,oauth2
from app.database import get_db
from typing import List,Optional

router = APIRouter(
     prefix="/expenses",
     tags = ['Expenses']
)

@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.ExpenseResponse])
async def get_expenses(db: AsyncSession = Depends(get_db), current_user  : models.User  = Depends(oauth2.get_current_user),Limit : int = 10, search : Optional[str] = ""):

    result = await db.execute(
        select(models.Expense)
        .where(models.Expense.owner_id == current_user.id)
        .where(models.Expense.description.contains(search))
        .limit(Limit)
    )
    all_expenses = result.scalars().all() 
    return all_expenses

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def get_expense_by_id(id: int , db : AsyncSession = Depends(get_db),current_user  : models.User  = Depends(oauth2.get_current_user)):

    result = await db.execute(
        select(models.Expense)
        .where(models.Expense.id == id)
    )
    expense = result.scalar_one_or_none() 

    if not expense:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found')

    if expense.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

    return expense

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ExpenseResponse)
async def post_expense(expenses : schemas.ExpenseCreate , db : AsyncSession = Depends(get_db), current_user : models.User  = Depends(oauth2.get_current_user)):

   new_expense = models.Expense(owner_id = current_user.id,**expenses.dict())
   db.add(new_expense)

   await db.commit()
   await db.refresh(new_expense)
   return new_expense

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(id : int , db : AsyncSession = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):

     result = await db.execute(
         select(models.Expense)
         .where(models.Expense.id == id)
     )
     expense_to_delete = result.scalar_one_or_none()

     if not expense_to_delete:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Expense with id = {id} not found')

     if expense_to_delete.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

     await db.delete(expense_to_delete) 
     await db.commit() 

@router.put("/{id}",status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def update_expense(id: int , expense : schemas.ExpenseCreate, db : AsyncSession = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):

    result = await db.execute(
        select(models.Expense)
        .where(models.Expense.id == id)
    )
    expense_result = result.scalar_one_or_none()

    if not expense_result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found')

    if expense_result.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

    for key, value in expense.dict().items():
        setattr(expense_result, key, value)

    await db.commit() 
    await db.refresh(expense_result) 
    return expense_result

