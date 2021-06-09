import json

import requests
from discord_webhook import DiscordWebhook, DiscordEmbed

from utils import config_parser, roles
from utils.roles import convert_server


class Appeal(object):
    def __init__(self, id, violator, server, date, author=None):
        self.id = int(id)
        self.violator = violator
        self.server = server
        self.date = date
        self.author = author
        self.author_img = f'https://excalibur-craft.ru/engine/ajax/lk/skin3d.php?mode=head&login={self.author}'
        self.url = f'https://excalibur-craft.ru/index.php?do=appeals&go=view&id={id}'


def compare_appeals(appeals: [Appeal]):
    appeals_ids = json.load(open('appeals.json', 'r'))
    new_appeals = list(filter(lambda x: x.id not in appeals_ids, appeals))
    json.dump(list(map(lambda x: x.id, new_appeals)), open('appeals.json', 'w'))
    return new_appeals


def appeal_to_webhook(appeal: Appeal):
    webhook = DiscordWebhook(url=config_parser.get_section_params('webhooks')['url'])
    embed = DiscordEmbed(title='**Подана новая жалоба на игрока**', color='FFD500')
    embed.add_embed_field(name='**Нарушитель**', value=f'{appeal.violator}', inline=False)
    embed.add_embed_field(name='**Сервер:**', value=f'{appeal.server}', inline=False)
    embed.add_embed_field(name='**Дата создания:**', value=f'{appeal.date}', inline=False)
    embed.add_embed_field(name='**Ссылка:**', value=f'[Нажми на меня]({appeal.url})', inline=False)
    embed.set_thumbnail(url='https://i.imgur.com/v94XnPf.png')
    embed.set_author(name=f'{appeal.author}', icon_url=f'{appeal.author_img}')
    embed.set_timestamp()

    webhook.content = f'<@&{roles.server_roles.get(convert_server(appeal.server))}>'
    webhook.add_embed(embed)
    webhook.execute()


def appeal_to_telegram(appeal: Appeal):
    users = json.load(open('config.json', 'r'))['users']
    for user in users:
        if appeal.server.replace(' ', '') in user['servers']:
            params = {
                'chat_id': user['chat_id'],
                'text': f'<b>Подана новая жалоба</b>\n<b>Нарушитель</b>: {appeal.violator}\n<b>Сервер</b>: {appeal.server}\n<b>Дата создания</b>: {appeal.date}\n<b>Автор</b>: {appeal.author}\n<b>Ссылка:</b> <a href="{appeal.url}">Нажми на меня</a>',
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            requests.get(f'https://api.telegram.org/bot{config_parser.get_section_params("telegram")["token"]}/sendMessage', params=params)
