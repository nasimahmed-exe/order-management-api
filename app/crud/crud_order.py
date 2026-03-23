from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model.order import Order
from app.model.lineItem import LineItem
from app.model.product import Product
from app.model.user import User
from app.schema.order import OrderCreate


def create_order(db: Session,*,obj_in: OrderCreate):
    user = db.query(User).filter(User.id == obj_in.user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    
    

    total_order_price = 0.0
    line_item_with_create = []

    for item_in in obj_in.items:
        product = db.query(Product).filter(Product.id == item_in.product_id).with_for_update().first()
        if not product or not product.is_available:
            raise HTTPException(status_code=404,detail="Product not found")
        
        
        

    total_price = product.price * item_in.quantity  
    total_order_price += total_price

    if user.balance < total_order_price:
        raise HTTPException(status_code=404,detail="Insufficent balance")
    
    user.balance -= total_order_price

    new_line_item = LineItem(
        product_id = product.id,
        quantity = item_in.quantity,
        price = product.price

    )
    line_item_with_create.append(new_line_item)

    db_order = Order(
        user_id = obj_in.user_id,
        billing_address = obj_in.billing_address,
        shipping_address = obj_in.shipping_address,
        total_price = total_order_price,
        items = line_item_with_create


    )
    if product.stock_quantity < item_in.quantity:
        raise HTTPException(status_code=404,detail = "out of stock")
    
    product.stock_quantity -= item_in.quantity

    db.add(db_order)
    db.flush()
    db.refresh(db_order)
    return db_order










  
            
            


            

            

            



 








  
                
        



    
        







