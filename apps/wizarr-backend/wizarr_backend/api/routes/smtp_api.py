from flask import request
from flask_jwt_extended import jwt_required, current_user
from flask_restx import Namespace, Resource
from playhouse.shortcuts import model_to_dict

from app.models.settings import SettingsGetModel, SettingsModel, SettingsPostModel
from app.models.database.settings import Settings

from helpers.smtp import send_invitation_email

api = Namespace("SMTP", description="SMTP related operations", path="/smtp")

@api.route("/send_invitation")
class SendEmailInvitation(Resource):
    """Discord related operations"""

    method_decorators = [jwt_required()]

    @api.doc(security="jwt")
    def post(self):
        """Update discord info"""
        # Get the discord token from the request

        code = request.json["code"]
        recipient = request.json["recipient"]

        # Check if the token is valid
        if not code:
            return { "message": f"Invalid code" }, 400
        
        if not recipient:
            return { "message": "Invalid recipient" }, 400

        # Check if any SMTP variables are invalid
        select_settings = Settings.select()
        settings = { setting.key: setting.value for setting in select_settings }

        smtp_address = settings["smtp_address"]
        smtp_port = settings["smtp_port"]
        smtp_username = settings["smtp_username"]
        smtp_password = settings["smtp_password"]

        if not smtp_address or not smtp_port or not smtp_username or not smtp_password:
            return { "message": f"Invalid SMTP connection credentials" }, 400

        if(send_invitation_email(recipient, code)):
             return { "message": f"Invitation sent to {recipient}" }, 200
        else:
             return { "message": f"Unable to send Invitation" }, 500
