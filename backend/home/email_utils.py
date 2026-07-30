import os
import logging
import threading
from email.utils import formataddr
from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.html import strip_tags
from .models import NotificationSetting, SiteGlobalSettings, FooterConfig
from .serializers import get_absolute_media_url

logger = logging.getLogger('django')


def get_dynamic_email_connection(config: NotificationSetting = None):
    """
    Constructs a Django Email Connection using CMS-stored SMTP parameters.
    Falls back to settings.py default connection if config is missing or inactive.
    """
    if not config or not config.smtp_host or not config.smtp_username:
        return get_connection(fail_silently=False)

    if config.smtp_port == 465:
        use_ssl = True
        use_tls = False
    elif config.smtp_port == 587:
        use_ssl = False
        use_tls = True
    else:
        use_tls = (config.encryption == NotificationSetting.EncryptionChoices.STARTTLS)
        use_ssl = (config.encryption == NotificationSetting.EncryptionChoices.SSL)

    return get_connection(
        backend='django.core.mail.backends.smtp.EmailBackend',
        host=config.smtp_host,
        port=config.smtp_port,
        username=config.smtp_username,
        password=config.smtp_password,
        use_tls=use_tls,
        use_ssl=use_ssl,
        timeout=config.timeout,
        fail_silently=False,
    )


def _get_logo_public_url(config: NotificationSetting = None):
    """
    Resolves the absolute public HTTPS URL for the AIEMS logo.
    Converts local dev host references (127.0.0.1 / localhost) to the public domain
    (https://api.aiems.edu.np) so cloud email clients (Gmail / Outlook) can fetch
    and render the logo over the internet.
    """
    public_url = None

    base_domain = getattr(settings, 'NEXT_PUBLIC_SITE_URL', 'https://api.aiems.edu.np').rstrip('/')
    if '127.0.0.1' in base_domain or 'localhost' in base_domain:
        base_domain = 'https://api.aiems.edu.np'

    try:
        # 1. Dedicated Email Logo
        if config and config.email_logo and bool(config.email_logo):
            public_url = get_absolute_media_url(None, config.email_logo)

        # 2. SiteGlobalSettings Logo
        if not public_url:
            site_settings = SiteGlobalSettings.objects.order_by('-created_at').first()
            if site_settings and site_settings.logo and bool(site_settings.logo):
                public_url = get_absolute_media_url(None, site_settings.logo)

        # 3. FooterConfig Logo
        if not public_url:
            footer_config = FooterConfig.objects.order_by('-created_at').first()
            if footer_config and footer_config.logo and bool(footer_config.logo):
                public_url = get_absolute_media_url(None, footer_config.logo)

    except Exception as ex:
        logger.error(f"[Email Engine] Error resolving logo public URL: {ex}")

    # Ensure full absolute URL
    if not public_url:
        public_url = f"{base_domain}/logo.png"
    elif public_url.startswith('/'):
        public_url = f"{base_domain}{public_url}"

    # SANITIZE LOCALHOST / 127.0.0.1 TO PUBLIC HTTPS DOMAIN
    if '127.0.0.1' in public_url or 'localhost' in public_url:
        if '/img/' in public_url:
            path_part = '/img/' + public_url.split('/img/')[-1]
            public_url = f"{base_domain}{path_part}"
        else:
            public_url = f"{base_domain}/logo.png"

    # Enforce HTTPS Protocol
    if public_url.startswith('http://'):
        public_url = public_url.replace('http://', 'https://', 1)

    return public_url


def test_smtp_connection(config=None):
    """
    Diagnostic helper to test active SMTP settings.
    """
    if not config:
        config = NotificationSetting.objects.filter(is_active=True).order_by('-created_at').first()

    if not config:
        return False, "No active NotificationSetting profile found in database."

    try:
        connection = get_dynamic_email_connection(config)
        connection.open()
        connection.close()
        return True, f"Successfully connected and authenticated with {config.smtp_host}:{config.smtp_port}!"
    except Exception as e:
        return False, f"SMTP Connection Error: {str(e)}"


def _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="200px"):
    """
    Renders clean, Outlook & Gmail compatible inline logo HTML table cell.
    Preserves natural aspect ratio without forcing dual width/height constraints.
    """
    if orientation == "vertical":
        size_attr = f'height="{max_dimension.replace("px", "")}"'
        constraint_style = f"height:{max_dimension}; width:auto; max-width:240px;"
    else:
        size_attr = f'width="{max_dimension.replace("px", "")}"'
        constraint_style = f"width:{max_dimension}; height:auto; max-height:80px;"

    return f"""<table role="presentation" border="0" cellspacing="0" cellpadding="0" align="center" style="margin:0 auto; text-align:center; border-collapse:collapse;">
        <tr>
            <td align="center" valign="middle" style="text-align:center; vertical-align:middle; padding:6px 0; border:0;">
                <img src="{logo_src}" alt="AIEMS" {size_attr} border="0" style="display:block; outline:none; text-decoration:none; border:0; margin:0 auto; {constraint_style}" />
            </td>
        </tr>
    </table>"""


def _format_template_body(template_str, context_dict):
    """
    Safely replaces plain text placeholders like {applicant_name}, {program_name}, {position_name},
    {contact}, {email}, {institution}, {city} without throwing KeyErrors.
    """
    if not template_str:
        return ""
    formatted = str(template_str)
    for key, value in context_dict.items():
        formatted = formatted.replace(f"{{{key}}}", str(value or ""))
    return formatted


# ==============================================================================
# PROFESSIONAL DYNAMIC HTML EMAIL TEMPLATE BUILDERS
# ==============================================================================
def _build_course_applicant_html(
    applicant_name, program_name, body_text, contact_phone,
    institution, from_email, logo_src, header_bg, footer_text,
    footer_address, next_steps_heading, next_steps_body
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="200px")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admission Application Received</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <!-- Header Banner with Protected Logo Card -->
                        <tr>
                            <td style="background: {header_bg}; padding: 32px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 10px 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); margin-bottom: 14px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <div style="display: inline-block; background-color: rgba(255,255,255,0.15); padding: 5px 14px; border-radius: 20px; color: #58bec6; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 10px; border: 1px solid rgba(88,190,198,0.3);">
                                    Admissions Desk
                                </div>
                                <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:800;">
                                    Application Received!
                                </h1>
                                <p style="color:#e2e8f0; margin:8px 0 0 0; font-size:14px; font-weight: 500;">
                                    {footer_text}
                                </p>
                            </td>
                        </tr>

                        <!-- Body Content -->
                        <tr>
                            <td style="padding: 32px 28px; background-color:#ffffff;">
                                <p style="font-size:16px; color:#0e0e54; margin:0 0 16px 0; font-weight:700;">
                                    Dear {applicant_name},
                                </p>
                                <p style="font-size:15px; color:#475569; line-height:1.7; margin:0 0 24px 0;">
                                    {body_text}
                                </p>

                                <!-- Submission Details Card -->
                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:12px; border-left:4px solid #009444; border-top:1px solid #e2e8f0; border-right:1px solid #e2e8f0; border-bottom:1px solid #e2e8f0; margin-bottom:28px;">
                                    <tr>
                                        <td style="padding: 20px;">
                                            <h4 style="margin:0 0 14px 0; color:#0e0e54; font-size:15px; font-weight:800; text-transform:uppercase; letter-spacing:0.5px;">
                                                Recorded Application Details
                                            </h4>
                                            <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0">
                                                <tr>
                                                    <td style="padding: 6px 0; font-size:14px; color:#64748b; width:140px;"><strong>Program:</strong></td>
                                                    <td style="padding: 6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{program_name}</td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 6px 0; font-size:14px; color:#64748b;"><strong>Contact Phone:</strong></td>
                                                    <td style="padding: 6px 0; font-size:14px; color:#1e293b;">{contact_phone}</td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 6px 0; font-size:14px; color:#64748b;"><strong>High School/College:</strong></td>
                                                    <td style="padding: 6px 0; font-size:14px; color:#1e293b;">{institution}</td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>

                                <!-- Next Steps Callout -->
                                {f'''<div style="background-color: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 12px; padding: 20px; margin-bottom: 28px;">
                                    <h5 style="margin: 0 0 8px 0; color: #166534; font-size: 14px; font-weight: 700;">
                                        {next_steps_heading}
                                    </h5>
                                    <p style="margin: 0; font-size: 13px; color: #15803d; line-height: 1.6;">
                                        {next_steps_body}
                                    </p>
                                </div>''' if next_steps_body else ''}

                                <p style="font-size:14px; color:#64748b; line-height:1.6; margin:0 0 24px 0;">
                                    Have urgent inquiries? Contact our admissions hotline or reply to <a href="mailto:{from_email}" style="color:#009444; font-weight:700; text-decoration:none;">{from_email}</a>.
                                </p>

                                <div style="text-align: center;">
                                    <a href="https://aiems.edu.np/contact-us" style="display: inline-block; background-color: #009444; color: #ffffff; text-decoration: none; font-size: 14px; font-weight: 700; padding: 12px 28px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 148, 68, 0.25);">
                                        Contact Counseling Desk
                                    </a>
                                </div>
                            </td>
                        </tr>

                        <!-- Footer -->
                        <tr>
                            <td style="background-color:#0e0e54; padding: 24px 30px; text-align: center; color:#94a3b8; font-size:12px; line-height:1.6;">
                                <p style="margin:0 0 6px 0; color:#ffffff; font-weight:700;">{footer_text}</p>
                                <p style="margin:0;">{footer_address} &bull; <a href="https://aiems.edu.np" style="color:#58bec6; text-decoration:none;">www.aiems.edu.np</a></p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_course_admin_html(
    applicant_name, gender, applicant_email, contact,
    program_name, institution, message, logo_src,
    header_bg, footer_text, footer_address
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="160px")

    message_html = ""
    if message and message != 'N/A':
        message_html = f'<div style="background-color:#fff1f2; border:1px solid #fecdd3; border-radius:8px; padding:14px; font-size:13px; color:#9f1239; margin-bottom:20px;"><strong>Applicant Message/Notes:</strong><br>{message}</div>'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>New Admission Application</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <tr style="background: {header_bg};">
                            <td style="padding: 28px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 8px 18px; border-radius: 12px; margin-bottom: 12px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <span style="background-color: #009444; color: #ffffff; font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 12px; letter-spacing: 1px;">
                                    NEW ADMISSION SUBMISSION
                                </span>
                                <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 20px; font-weight: 800;">
                                    {applicant_name}
                                </h2>
                                <p style="color: #cbd5e1; margin: 4px 0 0 0; font-size: 13px;">Target Degree: {program_name}</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 28px 24px;">
                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:10px; border:1px solid #e2e8f0; padding:16px; margin-bottom:20px;">
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b; width:130px;"><strong>Full Name:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{applicant_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Gender:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;">{gender}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Email:</strong></td>
                                        <td style="padding:6px 0; font-size:14px;"><a href="mailto:{applicant_email}" style="color:#009444; font-weight:700; text-decoration:none;">{applicant_email}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Phone:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;"><a href="tel:{contact}" style="color:#0e0e54; font-weight:700; text-decoration:none;">{contact}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Program:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{program_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>High School/College:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;">{institution}</td>
                                    </tr>
                                </table>

                                {message_html}

                                <div style="text-align: center; margin-top: 10px;">
                                    <a href="mailto:{applicant_email}?subject=Regarding%20your%20application%20to%20{footer_text}" style="display: inline-block; background-color: #0e0e54; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 10px 24px; border-radius: 6px;">
                                        Reply Directly to Applicant
                                    </a>
                                </div>
                            </td>
                        </tr>

                        <tr style="background-color: #f8fafc; border-top: 1px solid #e2e8f0;">
                            <td style="padding: 16px 30px; text-align: center; color: #94a3b8; font-size: 11px;">
                                Generated by {footer_text} Automated CMS Notification Dispatcher
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_job_applicant_html(
    applicant_name, position_name, body_text, contact_phone,
    from_email, logo_src, header_bg, footer_text, footer_address
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="200px")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Career Application Received</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <tr>
                            <td style="background: {header_bg}; padding: 32px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 10px 20px; border-radius: 12px; margin-bottom: 14px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <div style="display: inline-block; background-color: rgba(255,255,255,0.15); padding: 6px 16px; border-radius: 20px; color: #58bec6; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px; border: 1px solid rgba(88,190,198,0.3);">
                                    Human Resources Desk
                                </div>
                                <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:800;">
                                    Application Acknowledged
                                </h1>
                                <p style="color:#e2e8f0; margin:8px 0 0 0; font-size:14px;">
                                    {footer_text}
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 32px 28px;">
                                <p style="font-size:16px; color:#0e0e54; margin:0 0 16px 0; font-weight:700;">
                                    Dear {applicant_name},
                                </p>
                                <p style="font-size:15px; color:#475569; line-height:1.7; margin:0 0 24px 0;">
                                    {body_text}
                                </p>

                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:12px; border-left:4px solid #0e0e54; border:1px solid #e2e8f0; margin-bottom:28px;">
                                    <tr>
                                        <td style="padding: 20px;">
                                            <h4 style="margin:0 0 12px 0; color:#0e0e54; font-size:15px; font-weight:800;">
                                                Applied Position Summary
                                            </h4>
                                            <p style="margin:6px 0; font-size:14px; color:#475569;"><strong>Target Role:</strong> <span style="color:#0e0e54; font-weight:700;">{position_name}</span></p>
                                            <p style="margin:6px 0; font-size:14px; color:#475569;"><strong>Contact Phone:</strong> {contact_phone}</p>
                                            <p style="margin:6px 0; font-size:14px; color:#475569;"><strong>Status:</strong> <span style="color:#009444; font-weight:700;">Under HR Review</span></p>
                                        </td>
                                    </tr>
                                </table>

                                <p style="font-size:14px; color:#64748b; line-height:1.6; margin:0;">
                                    If your profile matches our requirements, our HR team will contact you directly to schedule an interview.
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="background-color:#0e0e54; padding: 24px 30px; text-align: center; color:#94a3b8; font-size:12px;">
                                {footer_text} &bull; {footer_address}
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_job_admin_html(
    applicant_name, gender, applicant_email, contact,
    position_name, document_url, message, logo_src,
    header_bg, footer_text, footer_address
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="160px")
    has_doc = bool(document_url and document_url != 'N/A' and document_url != '#')

    doc_button_html = ""
    if has_doc:
        doc_button_html = f'<a href="{document_url}" target="_blank" style="display: inline-block; background-color: #009444; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 12px 24px; border-radius: 8px; margin-right: 10px;">Download Resume / CV Document</a>'

    message_html = ""
    if message and message != 'N/A':
        message_html = f'<div style="background-color:#e0f2fe; border:1px solid #bae6fd; border-radius:8px; padding:14px; font-size:13px; color:#0369a1; margin-bottom:20px;"><strong>Cover Message:</strong><br>{message}</div>'

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>New Job Application</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <tr style="background: {header_bg};">
                            <td style="padding: 28px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 8px 18px; border-radius: 12px; margin-bottom: 12px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <span style="background-color: #58bec6; color: #0e0e54; font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 12px; letter-spacing: 1px;">
                                    NEW CAREER APPLICATION
                                </span>
                                <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 20px; font-weight: 800;">
                                    {applicant_name}
                                </h2>
                                <p style="color: #cbd5e1; margin: 4px 0 0 0; font-size: 13px;">Position Applied: {position_name}</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 28px 24px;">
                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:10px; border:1px solid #e2e8f0; padding:16px; margin-bottom:20px;">
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b; width:130px;"><strong>Candidate Name:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{applicant_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Gender:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;">{gender}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Email:</strong></td>
                                        <td style="padding:6px 0; font-size:14px;"><a href="mailto:{applicant_email}" style="color:#009444; font-weight:700; text-decoration:none;">{applicant_email}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Phone:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;"><a href="tel:{contact}" style="color:#0e0e54; font-weight:700; text-decoration:none;">{contact}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Target Role:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{position_name}</td>
                                    </tr>
                                </table>

                                {message_html}

                                <div style="text-align: center; margin-top: 20px;">
                                    {doc_button_html}
                                    <a href="mailto:{applicant_email}?subject=Regarding%20your%20Application%20for%20{position_name}" style="display: inline-block; background-color: #0e0e54; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 12px 24px; border-radius: 8px;">
                                        Contact Candidate
                                    </a>
                                </div>
                            </td>
                        </tr>

                        <tr style="background-color: #f8fafc; border-top: 1px solid #e2e8f0;">
                            <td style="padding: 16px 30px; text-align: center; color: #94a3b8; font-size: 11px;">
                                Generated by {footer_text} Automated HR Recruitment System
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_contact_applicant_html(
    applicant_name, body_text, from_email, logo_src,
    header_bg, footer_text, footer_address
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="200px")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Inquiry Received</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <tr>
                            <td style="background: {header_bg}; padding: 32px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 10px 20px; border-radius: 12px; margin-bottom: 14px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <h1 style="color:#ffffff; margin:0; font-size:24px; font-weight:800;">
                                    Inquiry Received
                                </h1>
                                <p style="color:#e2e8f0; margin:8px 0 0 0; font-size:14px;">
                                    {footer_text}
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 32px 28px;">
                                <p style="font-size:16px; color:#0e0e54; margin:0 0 16px 0; font-weight:700;">
                                    Dear {applicant_name},
                                </p>
                                <p style="font-size:15px; color:#475569; line-height:1.7; margin:0 0 24px 0;">
                                    {body_text}
                                </p>

                                <div style="background-color:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:16px; font-size:13px; color:#166534; line-height:1.6;">
                                    Our administrative staff will review your message and reply via email or phone call within 24 business hours.
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td style="background-color:#0e0e54; padding: 24px 30px; text-align: center; color:#94a3b8; font-size:12px;">
                                {footer_text} &bull; {footer_address}
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _build_contact_admin_html(
    applicant_name, applicant_email, contact, city,
    message, logo_src, header_bg, footer_text, footer_address
):
    logo_tag = _render_protected_logo_tag(logo_src, orientation="horizontal", max_dimension="160px")
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>New Website Inquiry</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
        <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f1f5f9; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:600px; background-color:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 10px 25px rgba(14, 14, 84, 0.08); border:1px solid #e2e8f0;">

                        <tr style="background: {header_bg};">
                            <td style="padding: 28px 24px; text-align: center;">
                                <div style="background-color: #ffffff; display: inline-block; padding: 8px 18px; border-radius: 12px; margin-bottom: 12px;">
                                    {logo_tag}
                                </div>
                                <br>
                                <span style="background-color: #009444; color: #ffffff; font-size: 10px; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 12px; letter-spacing: 1px;">
                                    WEBSITE INQUIRY
                                </span>
                                <h2 style="color: #ffffff; margin: 10px 0 0 0; font-size: 20px; font-weight: 800;">
                                    From {applicant_name} ({city})
                                </h2>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 28px 24px;">
                                <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border-radius:10px; border:1px solid #e2e8f0; padding:16px; margin-bottom:20px;">
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b; width:130px;"><strong>Name:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#0e0e54; font-weight:700;">{applicant_name}</td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Email:</strong></td>
                                        <td style="padding:6px 0; font-size:14px;"><a href="mailto:{applicant_email}" style="color:#009444; font-weight:700; text-decoration:none;">{applicant_email}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>Phone:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;"><a href="tel:{contact}" style="color:#0e0e54; font-weight:700; text-decoration:none;">{contact}</a></td>
                                    </tr>
                                    <tr>
                                        <td style="padding:6px 0; font-size:14px; color:#64748b;"><strong>City / Location:</strong></td>
                                        <td style="padding:6px 0; font-size:14px; color:#1e293b;">{city}</td>
                                    </tr>
                                </table>

                                <div style="background-color:#f1f5f9; border-left:4px solid #009444; border-radius:4px; padding:16px; font-size:14px; color:#334155; line-height:1.6; margin-bottom:20px;">
                                    <strong style="color:#0e0e54; display:block; margin-bottom:6px;">Inquiry Message:</strong>
                                    {message}
                                </div>

                                <div style="text-align: center; margin-top: 20px;">
                                    <a href="mailto:{applicant_email}?subject=RE:%20Your%20Inquiry%20to%20{footer_text}" style="display: inline-block; background-color: #0e0e54; color: #ffffff; text-decoration: none; font-size: 13px; font-weight: 700; padding: 12px 24px; border-radius: 8px;">
                                        Reply to Inquirer
                                    </a>
                                </div>
                            </td>
                        </tr>

                        <tr style="background-color: #f8fafc; border-top: 1px solid #e2e8f0;">
                            <td style="padding: 16px 30px; text-align: center; color: #94a3b8; font-size: 11px;">
                                {footer_text} Website Contact Desk Dispatcher
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """


def _send_protected_email(subject, html_content, text_content, from_email, to_emails, connection):
    """
    Constructs and dispatches clean, attachment-free HTML emails via Django's EmailMultiAlternatives.
    No binary images are attached to the message payload, keeping the email free of attachment paperclips.
    """
    to_list = to_emails if isinstance(to_emails, (list, tuple)) else [to_emails]

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=to_list,
        connection=connection
    )

    msg.attach_alternative(html_content, "text/html")

    try:
        connection.send_messages([msg])
    except Exception as primary_ex:
        logger.error(f"[Email Engine] Primary SMTP connection failed: {primary_ex}. Attempting fallback connection...")
        try:
            fallback_conn = get_connection(fail_silently=False)
            msg.connection = fallback_conn
            fallback_conn.send_messages([msg])
            logger.info("[Email Engine] Successfully dispatched email via fallback SMTP connection.")
        except Exception as fallback_ex:
            logger.error(f"[Email Engine] Fallback SMTP connection also failed: {fallback_ex}")
            raise fallback_ex


# ==============================================================================
# ASYNCHRONOUS THREADED DISPATCH WORKER
# ==============================================================================
def _async_send_email_task(submission_type: str, instance_data: dict):
    """
    Background thread worker that formats dynamic HTML/Text templates and dispatches
    both the Applicant Confirmation Email and Admin Alert Email over direct public HTTPS logo URLs.
    """
    try:
        config = NotificationSetting.objects.filter(is_active=True).order_by('-created_at').first()
        connection = get_dynamic_email_connection(config)

        # Resolve direct public HTTPS logo URL for clean inline rendering with zero attachments
        logo_src = _get_logo_public_url(config)

        # Extract Non-Technical Branding & Style Settings
        header_bg = (config.email_header_bg_color.strip() if config and config.email_header_bg_color else '') or '#0e0e54'
        if not (header_bg.startswith('#') or header_bg.startswith('rgb') or header_bg.startswith('linear')):
            header_bg = f"#{header_bg.lstrip('#')}"

        footer_text = (config.email_footer_text.strip() if config and config.email_footer_text else '') or 'Ankur Institute of Engineering and Management Studies (AIEMS)'
        footer_address = (config.email_footer_address.strip() if config and config.email_footer_address else '') or 'Bardibas, Mahottari, Nepal'
        next_steps_heading = (config.next_steps_heading.strip() if config and config.next_steps_heading else '') or 'What Happens Next?'
        next_steps_body = (config.next_steps_body.strip() if config and config.next_steps_body else '') or 'Our counseling team will verify your academic background and reach out with details regarding entrance schedules and fee structures.'

        # Build Default Sender Envelope with RFC 5322 formataddr
        clean_from = (config.default_from_email.strip() if config and config.default_from_email else '') or getattr(settings, 'DEFAULT_FROM_EMAIL', 'info@aiems.edu.np')
        sender_name = (config.default_sender_name.strip() if config and config.default_sender_name else '') or 'AIEMS Admissions & HR Desk'
        from_email = formataddr((sender_name, clean_from))

        # Resolve Admin Recipient Email List
        admin_emails = config.get_admin_email_list() if config else []
        if not admin_emails:
            site_settings = SiteGlobalSettings.objects.order_by('-created_at').first()
            if site_settings and site_settings.primary_email:
                admin_emails = [site_settings.primary_email.strip()]
        if not admin_emails:
            admin_emails = [clean_from]

        applicant_email = instance_data.get('email', '').strip()
        applicant_name = instance_data.get('name', 'Applicant').strip()

        # ----------------------------------------------------------------------
        # GENERATE TEMPLATES BASED ON SUBMISSION TYPE
        # ----------------------------------------------------------------------
        if submission_type == 'course':
            program_name = instance_data.get('program_name', 'BSc. CSIT / Academic Program')

            ctx = {
                'applicant_name': applicant_name,
                'name': applicant_name,
                'program_name': program_name,
                'program': program_name,
                'contact': instance_data.get('contact', 'N/A'),
                'phone': instance_data.get('contact', 'N/A'),
                'email': applicant_email,
                'institution': instance_data.get('institution', 'N/A'),
            }

            # 1. Applicant Email
            raw_subject = config.course_app_subject if (config and config.course_app_subject) else "Application Received: {program_name} at AIEMS"
            app_subject = _format_template_body(raw_subject, ctx)

            raw_body = config.course_app_applicant_body if (config and config.course_app_applicant_body) else "Thank you for applying to AIEMS. We have received your application details for the program. Our admissions counseling desk will review your submission and contact you shortly."
            app_body_text = _format_template_body(raw_body, ctx)

            app_html = _build_course_applicant_html(
                applicant_name=applicant_name,
                program_name=program_name,
                body_text=app_body_text,
                contact_phone=instance_data.get('contact', 'N/A'),
                institution=instance_data.get('institution', 'N/A'),
                from_email=clean_from,
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address,
                next_steps_heading=next_steps_heading,
                next_steps_body=next_steps_body
            )

            # 2. Admin Email
            admin_subject = f"[CMS Alert: New Admission] {applicant_name} - {program_name}"
            admin_html = _build_course_admin_html(
                applicant_name=applicant_name,
                gender=instance_data.get('gender', 'N/A'),
                applicant_email=applicant_email,
                contact=instance_data.get('contact', 'N/A'),
                program_name=program_name,
                institution=instance_data.get('institution', 'N/A'),
                message=instance_data.get('message', 'N/A'),
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address
            )

        elif submission_type == 'job':
            position_name = instance_data.get('position_name', 'Vacant Position')

            ctx = {
                'applicant_name': applicant_name,
                'name': applicant_name,
                'position_name': position_name,
                'position': position_name,
                'contact': instance_data.get('contact', 'N/A'),
                'phone': instance_data.get('contact', 'N/A'),
                'email': applicant_email,
            }

            # 1. Applicant Email
            raw_subject = config.job_app_subject if (config and config.job_app_subject) else "Application Received for {position_name} - AIEMS"
            app_subject = _format_template_body(raw_subject, ctx)

            raw_body = config.job_app_applicant_body if (config and config.job_app_applicant_body) else "Thank you for submitting your career application. Your resume and credentials have been delivered to our HR department for evaluation."
            app_body_text = _format_template_body(raw_body, ctx)

            app_html = _build_job_applicant_html(
                applicant_name=applicant_name,
                position_name=position_name,
                body_text=app_body_text,
                contact_phone=instance_data.get('contact', 'N/A'),
                from_email=clean_from,
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address
            )

            # 2. Admin Email
            admin_subject = f"[CMS Alert: New Job Application] {applicant_name} for {position_name}"
            admin_html = _build_job_admin_html(
                applicant_name=applicant_name,
                gender=instance_data.get('gender', 'N/A'),
                applicant_email=applicant_email,
                contact=instance_data.get('contact', 'N/A'),
                position_name=position_name,
                document_url=instance_data.get('document_url', '#'),
                message=instance_data.get('message', 'N/A'),
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address
            )

        else:  # Contact Inquiry
            ctx = {
                'applicant_name': applicant_name,
                'name': applicant_name,
                'contact': instance_data.get('contact', 'N/A'),
                'phone': instance_data.get('contact', 'N/A'),
                'email': applicant_email,
                'city': instance_data.get('city', 'N/A'),
            }

            # 1. Applicant Email
            raw_subject = config.contact_subject if (config and config.contact_subject) else "Inquiry Received - AIEMS Bardibas"
            app_subject = _format_template_body(raw_subject, ctx)

            raw_body = config.contact_applicant_body if (config and config.contact_applicant_body) else "Thank you for reaching out to AIEMS. We have received your inquiry message and our administration team will contact you soon."
            app_body_text = _format_template_body(raw_body, ctx)

            app_html = _build_contact_applicant_html(
                applicant_name=applicant_name,
                body_text=app_body_text,
                from_email=clean_from,
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address
            )

            # 2. Admin Email
            admin_subject = f"[CMS Alert: Contact Inquiry] From {applicant_name} ({instance_data.get('city', 'N/A')})"
            admin_html = _build_contact_admin_html(
                applicant_name=applicant_name,
                applicant_email=applicant_email,
                contact=instance_data.get('contact', 'N/A'),
                city=instance_data.get('city', 'N/A'),
                message=instance_data.get('message', 'N/A'),
                logo_src=logo_src,
                header_bg=header_bg,
                footer_text=footer_text,
                footer_address=footer_address
            )

        # DISPATCH APPLICANT CONFIRMATION EMAIL
        send_app = config.send_applicant_confirmation if config else True
        if send_app and applicant_email:
            _send_protected_email(
                subject=app_subject,
                html_content=app_html,
                text_content=strip_tags(app_html),
                from_email=from_email,
                to_emails=[applicant_email],
                connection=connection
            )

        # DISPATCH ADMIN NOTIFICATION EMAIL
        send_admin = config.send_admin_notification if config else True
        if send_admin and admin_emails:
            _send_protected_email(
                subject=admin_subject,
                html_content=admin_html,
                text_content=strip_tags(admin_html),
                from_email=from_email,
                to_emails=admin_emails,
                connection=connection
            )

        logger.info(f"[Email Engine] Successfully dispatched email(s) for '{submission_type}' submission #{instance_data.get('id')}.")

    except Exception as e:
        logger.error(f"[Email Engine] Exception encountered during '{submission_type}' email dispatch. Details: {str(e)}", exc_info=True)


def send_submission_emails_async(submission_type: str, instance_data: dict):
    """
    Public API function. Instantiates a non-blocking daemon thread to process email sending.
    """
    thread = threading.Thread(
        target=_async_send_email_task,
        args=(submission_type, instance_data),
        daemon=True
    )
    thread.start()