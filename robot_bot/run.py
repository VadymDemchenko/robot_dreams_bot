from tg_bot import app
from tg_bot.views import *
from tg_bot.contactbook_services import create_contacts_table

create_contacts_table()

app.run(host='0.0.0.0', port=4242, debug=True)



