from rest_framework.exceptions import APIException

class EmailSendingError(APIException):
    status_code = 500
    default_detail = "An error occurred while sending the email."
    default_code = "email_sending_error"

    def __init__(self, message, recipient):
        self.message = message
        self.recipient = recipient
        super().__init__(f"Failed to send email to {recipient}: {message}")

        
