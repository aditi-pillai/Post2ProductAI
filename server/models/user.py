from mongoengine import Document, StringField, DateTimeField, BooleanField, EmailField, ReferenceField, ListField
from datetime import datetime

class User(Document):
    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    instagram_connected = BooleanField(default=False)
    instagram_access_token = StringField()
    instagram_id = StringField()
    instagram_username = StringField()
    media = ListField(ReferenceField('Media'))
    products = ListField(ReferenceField('Product'))
    created_at = DateTimeField(default=datetime.utcnow)
    active = BooleanField(default=True)
    amazon_connected = BooleanField(default=False)
    amazon_seller_id = StringField()
    amazon_access_key = StringField()
    amazon_secret_key = StringField()
    
    # Shopify integration fields
    shopify_connected = BooleanField(default=False)
    shopify_shop_domain = StringField()
    shopify_access_token = StringField()

    meta = {
        'collection': 'users',
        'indexes': ['email']
    } 