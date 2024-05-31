PORT = 35000
SERVER_ADDRESS = "localhost"
LOG_FILENAME = "server.log"
LOG_LEVEL = 1
COMMAND_SIZE = 9
MAX_STR_SIZE = 20
INT_SIZE = 8
QUADX_OP = "quad_x   "
QUADY_OP = "quad_y   "
# new
PLAYER_OP ="player   "
UPDATE_OP = "update   "
GET_WALLS_OP ="get walls"
GET_BOMBS_OP ="get bombs"
START_GAME ="game     "
STEP_OP = "step     "
GET_OBJTS="get objts"

# new
NR_CLIENTS = 2

BYE_OP =  "bye      "
STOP_SERVER_OP = "stop    "
NR_QUAD_X = 20
NR_QUAD_Y = 20

import os

def load_map(file_path):
    with open(file_path, 'r') as file:
        return ''.join(line.strip() for line in file.readlines())


MAP_FILE_PATH = os.path.join(os.path.dirname(__file__), 'map.txt')
MAP = load_map(MAP_FILE_PATH)



