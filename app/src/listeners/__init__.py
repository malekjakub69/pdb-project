import threading
from src.listeners.test import start_test_listener


def register_listeners(mongo):
    test_listener_thread = threading.Thread(target=start_test_listener, args=(mongo,))
    test_listener_thread.start()
