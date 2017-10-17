def respond(user_id, message_text, attachment_type, attachment_url, postback, quick_reply, context):
    return dict(message_text='FAIL'), dict(conversation='test', stage='success')


def validate(message_text, attachment_type, postback, quick_reply):
et