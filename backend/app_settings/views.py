from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import redirect


def redirect_to_s3_view(request, asset_path):
    return redirect(static(asset_path))
