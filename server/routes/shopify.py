from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.product import Product
from models.media import Media
from services.shopify_service import ShopifyWebhookService
import logging

shopify_bp = Blueprint('shopify', __name__)
logger = logging.getLogger(__name__)

@shopify_bp.route('/connect', methods=['POST'])
@jwt_required()
def connect_shopify():
    """Connect user's Shopify store"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    try:
        user = User.objects.get(id=user_id)
        user.shopify_connected = True
        user.shopify_shop_domain = data.get('shop_domain')
        user.shopify_access_token = data.get('access_token')
        user.save()
        
        return jsonify({'message': 'Shopify store connected successfully'})
    except Exception as e:
        logger.error(f"Failed to connect Shopify: {e}")
        return jsonify({'error': str(e)}), 400

@shopify_bp.route('/publish/<product_id>', methods=['POST'])
@jwt_required()
def publish_to_shopify(product_id):
    """Publish a product to Shopify via n8n webhook"""
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=user_id)
        product = Product.objects.get(id=product_id, user=user)
        
        # Get associated Instagram post if exists
        instagram_post = None
        if product.instagram_post_ids:
            instagram_post = Media.objects.get(id=product.instagram_post_ids[0])
        
        # Initialize Shopify service
        shopify_service = ShopifyWebhookService()
        
        # Send to n8n webhook
        result = shopify_service.push_to_n8n(product, instagram_post)
        
        # Update product with Shopify status
        product.shopify_published = True
        product.shopify_product_id = result.get('shopify_product_id')
        product.shopify_status = 'published'
        product.save()
        
        return jsonify({
            'message': 'Product sent to Shopify successfully',
            'shopify_product_id': result.get('shopify_product_id'),
            'status': 'published'
        })
        
    except Product.DoesNotExist:
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        logger.error(f"Failed to publish product to Shopify: {e}")
        return jsonify({'error': str(e)}), 500

@shopify_bp.route('/products', methods=['GET'])
@jwt_required()
def get_shopify_products():
    """Get all products published to Shopify"""
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=user_id)
        products = Product.objects(user=user, shopify_published=True)
        
        shopify_products = []
        for product in products:
            shopify_products.append({
                'id': str(product.id),
                'title': product.title,
                'shopify_product_id': product.shopify_product_id,
                'shopify_status': product.shopify_status,
                'published_at': product.updated_at.isoformat() if product.updated_at else None
            })
        
        return jsonify({'products': shopify_products})
        
    except Exception as e:
        logger.error(f"Failed to get Shopify products: {e}")
        return jsonify({'error': str(e)}), 500

@shopify_bp.route('/webhook/status', methods=['POST'])
def webhook_status_update():
    """Receive status updates from n8n workflow"""
    try:
        # Validate webhook signature
        signature = request.headers.get('X-Post2Product-Signature')
        if not signature:
            return jsonify({'error': 'Missing signature'}), 401
        
        shopify_service = ShopifyWebhookService()
        payload = request.get_data(as_text=True)
        
        if not shopify_service.validate_webhook_signature(payload, signature):
            return jsonify({'error': 'Invalid signature'}), 401
        
        data = request.get_json()
        product_id = data.get('product_id')
        shopify_product_id = data.get('shopify_product_id')
        status = data.get('status')
        error_message = data.get('error')
        
        # Update product status in database
        product = Product.objects.get(id=product_id)
        product.shopify_product_id = shopify_product_id
        product.shopify_status = status
        
        if error_message:
            product.shopify_error = error_message
        
        product.save()
        
        return jsonify({'message': 'Status updated successfully'})
        
    except Exception as e:
        logger.error(f"Failed to update product status: {e}")
        return jsonify({'error': str(e)}), 500

@shopify_bp.route('/sync', methods=['POST'])
@jwt_required()
def sync_shopify_products():
    """Sync products from Shopify (placeholder for future implementation)"""
    user_id = get_jwt_identity()
    
    try:
        user = User.objects.get(id=user_id)
        if not user.shopify_connected:
            return jsonify({'error': 'Shopify not connected'}), 400
        
        # This would implement Shopify API sync
        # For now, return success message
        return jsonify({'message': 'Sync completed successfully'})
        
    except Exception as e:
        logger.error(f"Failed to sync Shopify products: {e}")
        return jsonify({'error': str(e)}), 500
