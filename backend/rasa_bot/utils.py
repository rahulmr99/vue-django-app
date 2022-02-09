from django.core.mail import send_mail
from django.template.loader import render_to_string

def send_fallback_notification(to, customer, fallback_message):
    message_view_link = "https://app.bookedfusion.com/#/messages"
    msg_plain = render_to_string('send_fallback.txt', {'fallback_message': fallback_message, 'message_view_link':message_view_link})
    msg_html = render_to_string('send_fallback.html', {'fallback_message': fallback_message, 'message_view_link':message_view_link})
    subject = "You have a new message from {}".format(customer)
    from_email = 'BookedFusion <noreply@bookedfusion.com>'
    
    send_mail(
        subject,
        msg_plain,
        from_email,
        [to],
        html_message = msg_html
    )
