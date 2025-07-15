from components.client_application import *

thread_condition = threading.Condition()

threads_pool: list[AsyncThread] = [AsyncThread(thread_condition) for i in range(CLIENT_MAX_CPU_CORE_USE)]
for thread in threads_pool:
    thread.start()

game = ClientApplication(0, True, threads_pool, thread_condition, WIDTH, HEIGHT)


game.players_pool.append(Player(PLAYER_NAME))
game.players_pool.append(Bot())
game.players_pool.append(Bot())
game.players_pool.append(Bot())
game.players_pool.append(Bot())

game.Run()

AsyncThread.thread_custom_join(threads_pool, thread_condition)
for thread in threads_pool:
    thread.close()
pg.quit()
exit()