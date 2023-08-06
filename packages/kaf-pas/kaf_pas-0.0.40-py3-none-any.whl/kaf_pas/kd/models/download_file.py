import logging

import requests
from django.conf import settings
from django.http import HttpResponseRedirect

from isc_common import ws

logger = logging.getLogger(__name__)


def download_attach_file(request, id):
    ws_channel = request.session.get('ws_channel')
    ws_port = request.session.get('ws_port')
    host = ws.WS_HOST

    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/DocumentsThumb/Download/{id}/', params=dict(port=ws_port, ws_channel=ws_channel, host=host))
    return HttpResponseRedirect(f'{settings.KOMPAS_INFORMICA}/logic/DocumentsThumb/Download/{id}/')


def download_attach_file_10(request, id):
    ws_channel = request.session.get('ws_channel')
    ws_port = request.session.get('ws_port')
    host = ws.WS_HOST

    r = requests.get(f'{settings.KOMPAS_INFORMICA}/logic/DocumentsThumb/Download10/{id}/', params=dict(port=ws_port, ws_channel=ws_channel, host=host))
    return HttpResponseRedirect(r.url)
