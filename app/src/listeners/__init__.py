import threading
from src.listeners.test import start_test_listener
from src.listeners.article import start_article_listener


def register_listeners(mongo):
    test_listener_thread = threading.Thread(target=start_test_listener, args=(mongo,))
    test_listener_thread.start()

    article_listener_thread = threading.Thread(target=start_article_listener, args=(mongo,))
    article_listener_thread.start()