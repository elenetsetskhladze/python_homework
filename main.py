from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
def get_products():
    return {"message": "product found"}

@app.post("/products")
def post_products():
    return {"message": "product created"}

@app.put("/products/{product_id}")
def update(product_id: int):
    return {"message": "product updated"}

@app.patch("/products/{product_id}")
def patch(product_id: int):
    return {"message": "product updated"}

@app.delete("/products/{product_id}")
def delete(product_id: int):
    return {"message": "product deleted"}

