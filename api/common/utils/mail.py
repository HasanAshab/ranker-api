from django.core.mail import (
    send_mail as dj_send_mail,
)
from django.template.loader import (
    render_to_string,
)
from django.utils.html import strip_tags


def send_mail(
    user,
    subject,
    message=None,
    fail_silently=None,
    template=None,
):
    html_message = None
    if template:
        html_message = render_to_string(
            template["path"],
            template["context"],
        )
        message = message if message else strip_tags(html_message)

    return dj_send_mail(
        subject=subject,
        message=message,
        from_email=None,
        html_message=html_message,
        recipient_list=[user.email],
        fail_silently=fail_silently,
    )
