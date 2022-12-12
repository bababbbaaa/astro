from databaseInteraction import *

for source in get_sources():
    print(source.payment_exists)