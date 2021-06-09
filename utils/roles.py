import re

server_roles = {
    'pixelmon': 852153088998768670,

    'classic': 852124256934428692,
    'revertingcapture': 852124256934428692,

    'industrial': 852152843637227530,
    'galaxy': 852152843637227530,

    'skyfactory': 852152957163012157,
    'galaxyv2': 852152957163012157,
    'gregtech': 852152957163012157,

    'rpg': 852152380497985536,
    'magic': 852152380497985536,
    'nevermine': 852152380497985536,

    'wonderland': 852152512307003432,

    'sandbox': 852153410890366987,

    'technomagic': 852152611640967198,

    'technomagicevo': 852152750401519618,

    'volcanoblock': 852153511821967390,
    'terrafirmacraft': 852153511821967390,

    'stalker': 852153292556861450
}


def convert_server(server):
    server = server.replace(' ', '').lower()
    return re.sub(r's\d', '', server)

