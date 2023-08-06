# Comagic dataapi v2 wrapper

# Installation

Install using `pip`...

    pip install comagic-wrapper

Or

    git clone https://github.com/bzdvdn/comagic-dataapi-wrapper.git

    python3 setup.py

#Doc
comagic doc - https://www.comagic.ru/support/api/data-api/

support full enpoints:
```python
(
    "calls_report", "communications_report", "virtual_numbers", "available_virtual_numbers",
    "sip_line_virtual_numbers", "sip_lines", "sip_line_password", "scenarios", "media_files",
    "campaigns","campaign_available_phone_numbers","campaign_available_redirection_phone_numbers",
    "campaign_parameter_weights", "sites", "site_blocks", "call_legs_report", "goals_report",
    "chats_report", "chat_messages_report", "offline_messages_report", "visitor_sessions_report",
    "financial_call_legs_report", "tags", "employees", "customers", "campaign_daily_stat",
)
```


# Usage

```python
from comagic import Comagic
client = Comagic("<login>", "<password>") # init retail api

or

client = Comagic(token="<token>")

# calls_report - endpoint, get - method, get data from get.calls_report
calls = client.calls_report.get(user_id="<user_id>", date_from="<date_from>", date_to="<date_to>")

# for creating something
site = client.sites.create(data={"<your params>"})
# delete
site  = client.sites.delete()

#update
site = client.sites.update(data={})

```