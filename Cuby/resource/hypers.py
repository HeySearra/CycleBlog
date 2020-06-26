import os

from Cuby.settings import MEDIA_ROOT

MAX_UPLOADED_FSIZE = 100 * 1024 * 1024
MAX_UPLOADED_FSIZE_DESC = f'{MAX_UPLOADED_FSIZE // (1024 * 1024)}MB'
DEFAULT_FILE_ROOT = os.path.join(MEDIA_ROOT, 'resource')
FNAME_DEFAULT_LEN = 20