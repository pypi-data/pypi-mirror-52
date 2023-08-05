# piano_sdk
Our Python SDK for Piano's API

# Usage examples
```
import piano_sdk

piano_sdk.aid = '<aid>'
piano_sdk.api_token = '<api_token>'


data = ('p7p3HxV20qHo3loRA36dJ1W2Y45taSpB7DXvJHImnuZuIre3j3x5HQ1B89YDWJkEIyWGCbsv_E25KqkV_8'
        '4v8VxgkxLaBEMqyOvNe_KSo1FDj7Upxv5Mgh8O7nGBEfQMVNE8XcbSKxwc-2kO4riLFoePVs9M4K3zMEmU'
        '5sJ7lKQL7S6bRsxm0MJtTV5gWEhKm85tPZcI2DewZVittlW1kOSAUBWzUPIO9iLh27n9CXKOUmbdXs4lAG'
        'O0U6ut_v2ApR-izNVo5mEzQygGsBCDWHvnmN2gx301XdM_vbGcfT0~~~NFxQCAc3j9Q7C_6j7z0P_wMSW3'
        'Lo22g1VlOdbvtNyj0')

descrypted = piano_sdk.SecurityUtils.decrypt(PRIVATE_KEY, data)

app = piano_sdk.App.retrieve('4Jqhagel8p')
apps = piano_sdk.App.list()

conversion = piano_sdk.Conversion.retrieve('TCC8DQTNPPK6')
conversions = piano_sdk.Conversion.list()

export = piano_sdk.Export.retrieve('URP2EVQIEEC3')
exports = piano_sdk.Export.list()

inquires = piano_sdk.Inquiry.list(uid='PNIIkVWiLprzb1b')

offer = piano_sdk.Offer.retrieve('OFU5ZE7R3O7U')
offers = piano_sdk.Offer.list()

promotion = piano_sdk.Promotion.retrieve('PN7BQW44LNMD')
promotions = piano_sdk.Promotion.list()

resource = piano_sdk.Resource.retrieve('BRDGIBNP')
resources = piano_sdk.Resource.list()

subscriptions = piano_sdk.Subscription.list()

offer_template = piano_sdk.OfferTemplate.retrieve('OTAI93QQ8MU5')
offer_templates = piano_sdk.OfferTemplate.list()

term = piano_sdk.Term.retrieve('TMQ93DOA69O3')
terms = piano_sdk.Term.list()

user = piano_sdk.User.retrieve('PNIIkVWiLprzb1b')
access_check = user.access_check(rid='BRDGIBNP')
accesses = user.access_list(access_id='7hOudV6FD1zZ')
subscriptions = user.subscriptions()
users = piano_sdk.User.list(limit=2)

for user in users.auto_paging_iter():
    print('{}: {} {}'.format(user['uid'], user['first_name'], user['last_name']))

webhook = piano_sdk.Webhook.retrieve('WERKQKWQYRSJYULWMCLA')
webhooks = piano_sdk.Webhook.list()
```
