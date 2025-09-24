from mongoengine import Document, StringField, DateTimeField, FloatField, ReferenceField, ListField, IntField, BooleanField
from datetime import datetime
from .user import User

class Product(Document):
    user = ReferenceField(User, required=True)
    asin = StringField(required=True)
    title = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    category = StringField()
    brand = StringField()
    image_urls = ListField(StringField())
    created_at = DateTimeField(default=datetime.utcnow)
    stock = IntField(default=0)
    instagram_post_ids = ListField(StringField())
    
    # Shopify integration fields
    shopify_published = BooleanField(default=False)
    shopify_product_id = StringField()
    shopify_status = StringField(default='draft')  # draft, published, failed
    shopify_error = StringField()
    tags = ListField(StringField())
    vendor = StringField()
    sku = StringField()
    
    meta = {
        'collection': 'products',
        'indexes': [
            'user',
            'asin',
            ('user', 'asin'),
        ]
    } 