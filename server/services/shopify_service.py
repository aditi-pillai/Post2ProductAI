import requests
import json
import hmac
import hashlib
from flask import current_app
from config import Config
import logging

logger = logging.getLogger(__name__)

class ShopifyWebhookService:
    def __init__(self):
        self.n8n_webhook_url = Config.N8N_WEBHOOK_URL
        self.webhook_secret = Config.WEBHOOK_SECRET
    
    def sign_payload(self, payload: dict) -> str:
        """Create HMAC signature for webhook payload"""
        body = json.dumps(payload, separators=(',', ':'), ensure_ascii=False).encode()
        return hmac.new(
            self.webhook_secret.encode(), 
            body, 
            hashlib.sha256
        ).hexdigest()
    
    def _prepare_images(self, image_urls: list) -> list:
        """Return image URLs as-is (must be public)"""
        return [u for u in (image_urls or []) if u]
    
    def create_shopify_payload(self, product, instagram_post=None):
        """Create payload for n8n webhook"""
        # Use provided image URLs as-is (ensure they are public/accessible)
        processed_images = self._prepare_images(getattr(product, 'image_urls', []) or [])
        
        payload = {
            "id": str(product.id),
            "title": product.title,
            "description": product.description or "",
            "price": str(product.price),
            "media_type": getattr(instagram_post, 'media_type', 'IMAGE') if instagram_post else 'IMAGE',
            "images": processed_images,
            "tags": getattr(product, 'tags', []),
            "vendor": getattr(product, 'vendor', "Post2Product"),
            "sku": getattr(product, 'sku', ""),
            "product_type": getattr(product, 'category', "General"),
            "inventory_quantity": getattr(product, 'stock', 0),
            "instagram_post_id": str(instagram_post.id) if instagram_post else None,
            "user_id": str(product.user.id)
        }
        
        return payload
    
    def push_to_n8n(self, product, instagram_post=None):
        """Send product data to n8n webhook for Shopify publishing"""
        try:
            payload = self.create_shopify_payload(product, instagram_post)
            
            # Create HMAC signature
            signature = self.sign_payload(payload)
            
            headers = {
                "Content-Type": "application/json",
                "X-Post2Product-Signature": signature,
                "User-Agent": "Post2ProductAI/1.0"
            }
            
            response = requests.post(
                self.n8n_webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Successfully sent product {product.id} to n8n")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send webhook to n8n: {e}")
            raise Exception(f"Webhook delivery failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in push_to_n8n: {e}")
            raise
    
    def create_payload_from_media(self, media, user=None):
        """Create a minimal Shopify payload directly from an Instagram media document."""
        caption = getattr(media, 'caption', '') or ''
        title = caption.strip().split('\n')[0][:120] if caption else f"Instagram Post {media.media_id}"
        images = self._prepare_images(getattr(media, 'media_url', []) or [])

        payload = {
            "id": getattr(media, 'media_id', None) or str(getattr(media, 'id', '')),
            "title": title or "Untitled",
            "description": caption,
            "price": "0.00",  # optional; can be edited later in Shopify
            "media_type": getattr(media, 'media_type', 'IMAGE') or 'IMAGE',
            "images": images,
            "tags": ["instagram", "post2product"],
            "vendor": getattr(user, 'name', None) or "Post2Product",
            "sku": "",
            "product_type": "General",
            "inventory_quantity": 0,
            "instagram_post_id": getattr(media, 'media_id', None),
            "user_id": str(getattr(user, 'id', '')) if user else None
        }
        return payload

    def push_media_to_n8n(self, media, user=None):
        """Send Instagram media data directly to n8n for Shopify publishing."""
        try:
            payload = self.create_payload_from_media(media, user)

            signature = self.sign_payload(payload)
            headers = {
                "Content-Type": "application/json",
                "X-Post2Product-Signature": signature,
                "User-Agent": "Post2ProductAI/1.0"
            }

            response = requests.post(
                self.n8n_webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()
            logger.info(f"Successfully sent media {payload.get('instagram_post_id')} to n8n")
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send media webhook to n8n: {e}")
            raise Exception(f"Webhook delivery failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in push_media_to_n8n: {e}")
            raise

    def validate_webhook_signature(self, payload: str, signature: str) -> bool:
        """Validate incoming webhook signature"""
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def get_shopify_product_status(self, product_id: str):
        """Check if product was successfully created in Shopify"""
        # This would typically query your database for the Shopify product ID
        # that was returned from the n8n workflow
        pass
