from flask import Blueprint, request, jsonify
from datetime import datetime
import requests
from models.user import User
from models.media import Media
from flask_jwt_extended import jwt_required
from services.shopify_service import ShopifyWebhookService

API_VERSION = "v20.0"

media_bp = Blueprint('media', __name__)

@media_bp.route('/media', methods=['GET'])
def get_instagram_media():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "Email required"}), 400

        user = User.objects(email=email).first()
        if not user or not user.instagram_connected:
            return jsonify({"error": "Instagram not connected"}), 400

        media_response = requests.get(
            f"https://graph.facebook.com/{API_VERSION}/{user.instagram_id}/media",
            params={
                "access_token": user.instagram_access_token,
                "fields": "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp"
            }
        )
        if media_response.status_code != 200:
            return jsonify({"error": "Failed to fetch media", "details": media_response.json()}), 400

        media_data = media_response.json().get('data', [])
        stored_media_ids = set(m.media_id for m in Media.objects(user_id=user))

        # Store new media in DB if not already present
        new_media_count = 0
        for item in media_data:
            if item['id'] not in stored_media_ids:
                media_doc = Media(
                    user_id=user,
                    media_id=item['id'],
                    media_type=item.get('media_type', ''),
                    media_url=[item.get('media_url')] if item.get('media_url') else [],
                    caption=item.get('caption', ''),
                    created_at=datetime.fromisoformat(item['timestamp'].replace('Z', '+00:00')) if item.get('timestamp') else datetime.utcnow()
                )
                media_doc.save()
                user.update(push__media=media_doc)
                new_media_count += 1

                # Trigger n8n webhook for image posts only
                try:
                    if media_doc.media_type == 'IMAGE' and media_doc.media_url:
                        shopify_service = ShopifyWebhookService()
                        # Only trigger if webhook URL is configured
                        if shopify_service.n8n_webhook_url:
                            shopify_service.push_media_to_n8n(media_doc, user)
                except Exception:
                    # Do not fail the whole request if webhook fails; continue
                    pass

        return jsonify({
            "media": media_data,
            "new_media_stored": new_media_count
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@media_bp.route('/media/local', methods=['GET'])
def get_local_media():
    try:
        email = request.args.get('email')
        if not email:
            return jsonify({"error": "Email required"}), 400

        user = User.objects(email=email).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        media_list = Media.objects(user_id=user)
        return jsonify({
            "media": [{
                "id": str(m.id),
                "media_id": m.media_id,
                "media_type": m.media_type,
                "media_url": m.media_url,
                "caption": m.caption,
                "hashtags": m.hashtags,
                "likes": m.likes,
                "comments": m.comments,
                "created_at": m.created_at.isoformat()
            } for m in media_list]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@media_bp.route('/media/<media_id>', methods=['GET'])
@jwt_required()
def get_media_details(media_id):
    """Get details for a specific media item"""
    access_token = request.headers.get('Instagram-Access-Token')
    if not access_token:
        return jsonify({"error": "No access token provided"}), 400

    try:
        response = requests.get(
            f"https://graph.instagram.com/{media_id}",
            params={
                'fields': 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp',
                'access_token': access_token
            }
        )
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@media_bp.route('/media/analyze', methods=['POST'])
@jwt_required()
def analyze_media():
    """Analyze media for product potential"""
    data = request.get_json()
    media_url = data.get('media_url')
    caption = data.get('caption')

    if not media_url:
        return jsonify({"error": "No media URL provided"}), 400

    # Here you would implement your media analysis logic
    # This is a placeholder for the actual implementation
    analysis_result = {
        "media_url": media_url,
        "caption": caption,
        "product_potential": "high",
        "suggested_categories": ["fashion", "lifestyle"],
        "confidence_score": 0.85
    }

    return jsonify(analysis_result) 