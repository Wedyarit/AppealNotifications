import time

from ex_parser import parsers
from ex_parser.authentication.authenticator import Authenticator
from utils import appeal


def main():
    authenticator = Authenticator()

    while True:
        authenticator.validate()
        site_appeals = parsers.appeals()
        if site_appeals is None:
            continue
        appeals = appeal.compare_appeals(site_appeals)
        parsers.fill_in_appeals(appeals)
        list(map(appeal.appeal_to_webhook, appeals))
        list(map(appeal.appeal_to_telegram, appeals))
        time.sleep(60 * 2)


if __name__ == '__main__':
    main()
