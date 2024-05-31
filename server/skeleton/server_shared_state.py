import threading
from server_impl.gamemech import GameMech
import server_impl

class ServerSharedState:
    def __init__(self, gamemech: GameMech):
        self._nr_connections = 0
        self._connections_lock = threading.Lock()
        self._start_game = False
        self._start_game_sem = threading.Semaphore(0)
        self._gamemech = gamemech

    def add_client(self):
        with self._connections_lock:
            self._nr_connections += 1
        # Testar e ja existem numero suficiente de clientes!
        if self._nr_connections == server_impl.NR_CLIENTS:
            with self._connections_lock:
                self._start_game = True
                for i in range(self._nr_connections):
                    self._start_game_sem.release()

    def get_objects(self) -> dict:
        with self._connections_lock:
            res = self._gamemech.get_players()
        return res

    def start_game_sem(self):
        return self._start_game_sem

    def gamemech(self):
        return self._gamemech

    #@property
    def start_game(self):
        return self._start_game
