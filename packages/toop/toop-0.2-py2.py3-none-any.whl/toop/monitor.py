import requests
import os
import time
from termcolor import cprint
from pyfiglet import Figlet



def monitor(website_url, interval):
    """
    monitors the status of the input website

    :param website_url: the website to monitor/visit
    :type website_url: string

    :param interval: the number of times the website should be visited
    :type special_words: integer

    :returns: A command line response and notification indicating the
            status of the site on each visit
    """
    title = Figlet(font="slant")
    cprint(title.renderText("toop toop toop :"), "blue", attrs=['bold'])

    for i in range(1, interval + 1):
        try:
            req = requests.get(website_url)
            req.raise_for_status()
            message = "LIVE♥️!"
            resp_color = "green"
        except Exception as error:
            message = f'Error : {error}'
            resp_color = "red"
        finally:
            cprint(
                f"Interval {i} : Tooping {website_url} -> Status -> {message}", f"{resp_color}")
            title = '-title {!r}'.format(f'Status for {website_url}:')
            message = '-message {!r}'.format(message)
            os.system(
                'terminal-notifier {}'.format(' '.join([message, title])))
            cprint("========================================", "blue")
            time.sleep(10)  # sleep for 10 seconds before making next request
