from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
# CHANGED: Removed synchronous Session import, now using AsyncSession for async DB operations
# from sqlalchemy.orm import sessionmaker,Session
from sqlalchemy.future import select  # NEW: SQLAlchemy 2.0 async style queries
from sqlalchemy.ext.asyncio import AsyncSession  # NEW: Async session for non-blocking DB calls
from app import models,schemas,utils,oauth2
from app.database import get_db
from typing import List,Optional

router = APIRouter(
     prefix="/expenses",
     tags = ['Expenses']
)

# CHANGED: db parameter type from Session to AsyncSession
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


# CHANGED: db parameter type from Session to AsyncSession
@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def get_expense_by_id(id: int , db : AsyncSession = Depends(get_db),current_user  : models.User  = Depends(oauth2.get_current_user)):
    # CHANGED: Using await db.execute(select().where()) instead of db.query().filter().first()
    # This is async and won't block other requests
    result = await db.execute(
        select(models.Expense)
        .where(models.Expense.id == id)
    )
    expense = result.scalar_one_or_none()  # NEW: scalar_one_or_none() gets first result or None
    # OLD: expense_by_id = db.query(models.Expense).filter(models.Expense.id == id).first()
    # OLD: This blocked the entire worker thread while waiting for DB

    #.first() gets the first one and returns a single model object
    #.all() returns a list of model objects
    if not expense:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found')

    if expense.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

    return expense



# CHANGED: db parameter type from Session to AsyncSession
@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ExpenseResponse)
async def post_expense(expenses : schemas.ExpenseCreate , db : AsyncSession = Depends(get_db), current_user : models.User  = Depends(oauth2.get_current_user)):
  #new_expense = models.Expense(expense = expenses.expense , description = expenses.description, mode = expenses.mode) #Creating an expense object
  #What if we have 50 attributes in the table, instead of doing that we can do dictionary unpacking
   new_expense = models.Expense(owner_id = current_user.id,**expenses.dict()) #dictionary unpacking
   db.add(new_expense) #adding the expense to our database
   # CHANGED: db.commit() and db.refresh() are now awaited because they're async operations
   await db.commit() #commiting the changes - ASYNC: must await because it writes to DB
   await db.refresh(new_expense) #represents the returning * statement - ASYNC: must await
   return new_expense #Is a sqlalchemymodel not a dict, and pydantic models only work with dictionary

# CHANGED: db parameter type from Session to AsyncSession
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(id : int , db : AsyncSession = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):

     # CHANGED: Using select().where() with await instead of query().filter()
     result = await db.execute(
         select(models.Expense)
         .where(models.Expense.id == id)
     )
     expense_to_delete = result.scalar_one_or_none()
     # OLD: expense_query = db.query(models.Expense).filter(models.Expense.id == id)
     # OLD: expense_result = expense_query.first()
     # OLD: This was synchronous and blocked the thread

     #.find() here will return the data to the api, so I cant delete it on the db,
     #without the .find() or .all() the query is still ongoing with the db on which I can act to delete the data
     if not expense_to_delete:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Expense with id = {id} not found')

     if expense_to_delete.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

     # CHANGED: Using await db.delete() and await db.commit() instead of query.delete()
     await db.delete(expense_to_delete)  # ASYNC: marks for deletion
     await db.commit()  # ASYNC: actually commits the deletion to DB
     # OLD: expense_query.delete(synchronize_session = False)
     # OLD: db.commit()

# CHANGED: db parameter type from Session to AsyncSession (also fixed type hint: was "int", now "models.User")
@router.put("/{id}",status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def update_expense(id: int , expense : schemas.ExpenseCreate, db : AsyncSession = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):
    # CHANGED: Using select().where() with await instead of query().filter()
    result = await db.execute(
        select(models.Expense)
        .where(models.Expense.id == id)
    )
    expense_result = result.scalar_one_or_none()
    # OLD: expense_query = db.query(models.Expense).filter(models.Expense.id == id)
    # OLD: expense_result = expense_query.first()

    if not expense_result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found')

    if expense_result.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

    # CHANGED: Instead of query.update() with dict, we manually set attributes then commit
    # This is the recommended pattern for async SQLAlchemy
    for key, value in expense.dict().items():
        setattr(expense_result, key, value)

    await db.commit()  # ASYNC: must await the commit
    await db.refresh(expense_result)  # ASYNC: refresh to get updated values
    return expense_result
    # OLD: expense_query.update(expense.dict(), synchronize_session = False)
    # OLD: db.commit()
    # OLD: return expense_result
