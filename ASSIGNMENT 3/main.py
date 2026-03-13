from fastapi import FastAPI, Response, status, Query, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

##database
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": False},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True}
]
## Question1 : Add  New Products 
from fastapi import HTTPException

class ProductCreate(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool
  
@app.post("/products", status_code=201)
def add_product(product: ProductCreate):

    # check duplicate product name
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(
                status_code=400,
                detail="Product with this name already exists"
            )

    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }
  
## Question2 : update Product(PUT)
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = None,
    in_stock: Optional[bool] = None
):

    for product in products:

        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {
                "message": "Product updated",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")

## Question3 : Delete a Product
@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:

        if product["id"] == product_id:

            products.remove(product)

            return {
                "message": f"Product '{product['name']}' deleted"
            }

    raise HTTPException(status_code=404, detail="Product not found")

## Question5 :  Inventory Summary
@app.get("/products/audit")
def product_audit():

    total_products = len(products)

    in_stock_products = [p for p in products if p["in_stock"]]

    out_stock_names = [
        p["name"] for p in products if not p["in_stock"]
    ]

    total_value = sum(p["price"] * 10 for p in in_stock_products)

    most_expensive = max(products, key=lambda p: p["price"])

    return {
        "total_products": total_products,
        "in_stock_count": len(in_stock_products),
        "out_of_stock_names": out_stock_names,
        "total_stock_value": total_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }

## Question4 : Full CRUD Sequence 
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:

        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")

## bonus :
@app.put("/products/discount")
def apply_discount(category: str, discount_percent: int):

    updated = []

    for product in products:

        if product["category"].lower() == category.lower():

            new_price = int(
                product["price"] * (1 - discount_percent / 100)
            )

            product["price"] = new_price

            updated.append({
                "name": product["name"],
                "new_price": new_price
            })

    if not updated:
        return {"message": "No products found in this category"}

    return {
        "updated_products": updated,
        "count": len(updated)
    }
