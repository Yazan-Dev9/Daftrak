from models.product import Product
from models.user import User
from sqlalchemy.orm import Session


class UserCRUD:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user(
        self, name, birth_date, email, password, phone=None, address=None, role=None
    ):
        user = User(
            name=name,
            birth_date=birth_date,
            email=email,
            password=password,  # يفضل التشفير هنا
            phone=phone,
            address=address,
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_users(self):
        return self.db.query(User).all()

    def get_user_by_email(self, email):
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id):
        return self.db.query(User).filter(User.id == user_id).first()

    def update_user(
        self, user_id, name, birth_date, email, password, phone, address, role
    ):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = name
            user.birth_date = birth_date
            user.email = email
            user.password = password
            user.phone = phone
            user.address = address
            user.role = role
            self.db.commit()
            self.db.refresh(user)
            return user
        return None

    def delete_user(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False


class ProductCRUD:
    def __init__(self, db_session: Session):
        self.db = db_session

    def create_product(self, name, category, quantity, price, cost, description):
        product = Product(
            name=name,
            category=category,
            quantity=quantity,
            price=price,
            cost=cost,
            description=description,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_products_by_category(self, category):
        return self.db.query(Product).filter(Product.category == category).all()

    def get_products_by_name(self, name):
        return self.db.query(Product).filter(Product.name == name).all()

    def get_products_by_price(self, price):
        return self.db.query(Product).filter(Product.price == price).all()

    def get_products_by_cost(self, cost):
        return self.db.query(Product).filter(Product.cost == cost).all()

    def get_products_by_quantity(self, quantity):
        return self.db.query(Product).filter(Product.quantity == quantity).all()

    def get_products_by_made_date(self, made_date):
        return self.db.query(Product).filter(Product.made_date == made_date).all()

    def get_products_by_exp_date(self, exp_date):
        return self.db.query(Product).filter(Product.exp_date == exp_date).all()

    def update_product(
        self, product_id, name, category, quantity, price, cost, description
    ):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.name = name
            product.category = category
            product.quantity = quantity
            product.price = price
            product.cost = cost
            product.description = description
            self.db.commit()
            self.db.refresh(product)
            return product
        return None

    def delete_product(self, product_id):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            self.db.delete(product)
            self.db.commit()
            return True
        return False

