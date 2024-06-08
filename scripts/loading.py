import sys
import os

loading_icon = ['|', '\\', '-', '/']
progress = 50 
amount = 188
message = "Downloading somthing"
precent = int((progress / amount) * 100)
precent_msg = f" {precent}% "
term_size_width = (os.get_terminal_size()[0] // 2) - 2 - len(precent_msg)

msg_string = f"[{loading_icon[1]}] {message}"
msg_string += (os.get_terminal_size()[0] // 2 - len(msg_string)) * ' '
if os.get_terminal_size()[0] % 2:
    msg_string += ' '
# [/] Downloading [####----] 50%

progress_bar = ((term_size_width - precent) * '-')

remaining = (term_size_width - len(progress_bar)) * '#' 


sys.stdout.write(f"{msg_string}[{remaining}{progress_bar}]{precent_msg}")
sys.stdout.flush()
