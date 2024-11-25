from .start import handler as start_handler
from .request_access import handler as request_access_handler
from .admin_commands import approve_handler, reject_handler
from .set_path import conv_handler as set_path_conv_handler
from .get_path import handler as get_path_handler
from .save_file import handler as save_file_handler
from .save_photo import handler as save_photo_handler
from .save_video import handler as save_video_handler

start = start_handler
request_access = request_access_handler
admin_commands = (approve_handler, reject_handler)
set_path = set_path_conv_handler
get_path = get_path_handler
save_file = save_file_handler
save_photo = save_photo_handler
save_video = save_video_handler