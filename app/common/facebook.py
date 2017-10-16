def send_message(sender_id, text=None, attachment=None, quick_replies=None, buttons=None, metadata=None, action=None,
                 notification_type='REGULAR'):
    from app.settings import FACEBOOK_TOKEN
    import requests

    data = dict(
        recipient=dict(id=sender_id),
        notification_type=notification_type,
    )
    if text or attachment:
        data['message'] = {k: v for k, v in
                           dict(text=text, attachment=attachment, quick_replies=quick_replies, metadata=metadata,
                                buttons=buttons) if v}
    elif action in ['typing_on', 'typing_off', 'mark_seen']:
        data['sender_action'] = action

    r = requests.post(
        url='https://graph.facebook.com/v2.6/me/messages?access_token={0}'.format(FACEBOOK_TOKEN), json=data
    )
    return r


def update_messenger_profile(persistent_menu=None, get_started=None, greeting=None, home_url=None):
    from app.settings import FACEBOOK_TOKEN
    import requests
    data = {
        k: v for k, v in
        dict(
            persistent_menu=persistent_menu,
            get_started=get_started,
            greeting=greeting,
            home_url=home_url
        ).items() if v
    }
    r = requests.post(
        url='https://graph.facebook.com/v2.6/me/messenger_profile?access_token={0}'.format(FACEBOOK_TOKEN),
        json=data
    )
    return r
