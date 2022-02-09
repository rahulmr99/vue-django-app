# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-13 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_settings', '0013_generalsettings_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackconfig',
            name='email_tmpl',
            field=models.TextField(default='<table style="max-width:650px;padding:30px 10px;" class="container" width="100%" cellspacing="0" cellpadding="0"\n       border="0" align="center">\n    <tbody>\n    <tr>\n        <td style="padding:20px 25px !important;margin:0;border:1px solid #efefef;border-radius:3px;"\n            class="padding-wrapper" bgcolor="#ffffff">\n            <table width="100%" cellspacing="0" cellpadding="0">\n                <tbody>\n                <tr>\n                    <td style="padding:25px 0 10px 0 !important;font-size:18px;line-height:25px;font-family:sans-serif;text-align:left;color:#999999;">\n                        Hi {{ name }}\n                    </td>\n                </tr>\n                <tr>\n                    <td style="padding:10px 0 10px 0 !important;font-size:16px;line-height:25px;font-family:sans-serif;color:#999999;">\n                        Thanks for coming in today! Please help us to understand how we\'re doing. Rate your experience\n                        below.\n                    </td>\n                </tr>\n                </tbody>\n            </table>\n            <table width="100%" cellspacing="0" cellpadding="0">\n                <tbody>\n                <tr>\n                    <td colspan="2"\n                        style="padding:10px 0 10px 0 !important;font-size:16px;line-height:25px;font-family:sans-serif;color:#999999;"\n                        class="custom-confirmation" align="left">Thank you, your appointment has been successfully\n                        scheduled.\n                    </td>\n                </tr>\n                </tbody>\n            </table>\n            <p>\n                <br>\n            </p>\n            <hr style="border:1px solid #efefef;">\n            <p>\n                <br>\n            </p>\n            <table cellspacing="5" cellpadding="0" border="0" align="center">\n                <tbody>\n                <tr>\n                    <td style=\'valign="middle" align="center"\'>\n                        <a href="{{ feedback_link }}../1/"\n                           style="color:#FFC107 !important;text-decoration:none !important; font-size: 50px;">\n                            <img src="https://s3.amazonaws.com/bookedfusion.com/images/Angry_Emoji.png" width="50"\n                                 height="50"/>\n                        </a>\n                    </td>\n                    <td style=\'valign="middle" align="center"\'>\n                        <a href="{{ feedback_link }}../2/"\n                           style="color:#FFC107 !important;text-decoration:none !important; font-size: 50px;">\n                            <img src="https://s3.amazonaws.com/bookedfusion.com/images/Very_sad_emoji.png" width="50"\n                                 height="50"/>\n                        </a>\n                    </td>\n                    <td style=\'valign="middle" align="center"\'>\n                        <a href="{{ feedback_link }}../3/"\n                           style="color:#FFC107 !important;text-decoration:none !important; font-size: 50px;">\n                            <img src="https://s3.amazonaws.com/bookedfusion.com/images/Neutral_Face.png" width="50"\n                                 height="50"/>\n                        </a>\n                    </td>\n                    <td style=\'valign="middle" align="center"\'>\n                        <a href="{{ feedback_link }}../4/"\n                           style="color:#FFC107 !important;text-decoration:none !important; font-size: 50px;">\n                            <img src="https://s3.amazonaws.com/bookedfusion.com/images/smile_emoji.png" width="50"\n                                 height="50"/>\n                        </a>\n                    </td>\n                    <td style=\'valign="middle" align="center"\'>\n                        <a href="{{ feedback_link }}../5/"\n                           style="color:#FFC107 !important;text-decoration:none !important; font-size: 50px;">\n                            <img src="https://s3.amazonaws.com/bookedfusion.com/images/Heart_Eyes_Emoji.png" width="50"\n                                 height="50"/>\n                        </a>\n                    </td>\n                </tr>\n                </tbody>\n            </table>\n        </td>\n    </tr>\n    </tbody>\n</table>\n'),
        ),
    ]
