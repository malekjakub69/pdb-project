import threading
from src.listeners.test import start_test_listener
from src.listeners.article import start_article_listener
from src.listeners.comment import start_comment_listener
from src.listeners.user import start_user_listener
from src.listeners.like import start_like_listener
from src.listeners.read import start_read_listener


def register_listeners(mongo):
    test_listener_thread = threading.Thread(target=start_test_listener, args=(mongo,))
    test_listener_thread.start()

    article_listener_thread = threading.Thread(target=start_article_listener, args=(mongo,))
    article_listener_thread.start()

    comment_listener_thread = threading.Thread(target=start_comment_listener, args=(mongo,))
    comment_listener_thread.start()

    user_listener_thread = threading.Thread(target=start_user_listener, args=(mongo,))
    user_listener_thread.start()

    like_listener_thread = threading.Thread(target=start_like_listener, args=(mongo,))
    like_listener_thread.start()

    read_listener_thread = threading.Thread(target=start_read_listener, args=(mongo,))
    read_listener_thread.start()