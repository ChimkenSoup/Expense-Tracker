from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from sqlalchemy.orm import sessionmaker,Session
from app import models,schemas,utils,oauth2
from app.database import get_db
from typing import List,Optional

router = APIRouter(
     prefix="/expenses",
     tags = ['Expenses']
)

@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.ExpenseResponse])
async def get_expenses(db: Session = Depends(get_db), current_user  : models.User  = Depends(oauth2.get_current_user),Limit : int = 10, search : Optional[str] = ""):
        all_expenses = db.query(models.Expense).filter(models.Expense.owner_id == current_user.id, models.Expense.description.contains(search)).limit(Limit).all()
        #db.query(models.Expense) translates to the query and is connected to the db
        #.all() fires the query and returns the data
        return all_expenses
                    

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def get_expense_by_id(id: int , db : Session = Depends(get_db),current_user  : models.User  = Depends(oauth2.get_current_user)):
    expense_by_id = db.query(models.Expense).filter(models.Expense.id == id).first()
    #.first() gets the first one and returns a single model object
    #.all() returns a list of model objects
    if not expense_by_id:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found')
    
    if expense_by_id.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")

    return expense_by_id
     


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.ExpenseResponse)
async def post_expense(expenses : schemas.ExpenseCreate , db : Session = Depends(get_db), current_user : models.User  = Depends(oauth2.get_current_user)):
  #new_expense = models.Expense(expense = expenses.expense , description = expenses.description, mode = expenses.mode) #Creating an expense object
  #What if we have 50 attributes in the table, instead of doing that we can do dictionary unpacking
   new_expense = models.Expense(owner_id = current_user.id,**expenses.dict()) #dictionary unpacking
   db.add(new_expense) #adding the expense to our database
   db.commit() #commiting the changes
   db.refresh(new_expense) #represents the returning * statement
   return new_expense #Is a sqlalchemymodel not a dict, and pydantic models only work with dictionary 

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_expense(id : int , db : Session = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):

     expense_query = db.query(models.Expense).filter(models.Expense.id == id) 

     expense_result = expense_query.first()
    
     #.find() here will return the data to the api, so I cant delete it on the db,
     #without the .find() or .all() the query is still ongoing with the db on which I can act to delete the data
     if not expense_result:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Expense with id = {id} not found')
     
     if expense_result.owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")
     
     expense_query.delete(synchronize_session = False)
     db.commit()

@router.put("/{id}",status_code = status.HTTP_200_OK, response_model = schemas.ExpenseResponse)
async def update_expense(id: int , expense : schemas.ExpenseCreate, db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    expense_query = db.query(models.Expense).filter(models.Expense.id == id)

    expense_result = expense_query.first()

    if not expense_result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Expense with id = {id} not found') 
    
    if expense_query.first().owner_id != current_user.id:
          raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail = "Not authorized to perform requested action")
    
    expense_query.update(expense.dict(), synchronize_session = False)
    db.commit()
    return expense_result