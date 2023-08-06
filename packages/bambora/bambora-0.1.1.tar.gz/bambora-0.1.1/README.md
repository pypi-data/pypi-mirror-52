Bambora Client
==============

![PyPi](https://img.shields.io/badge/python-2.7%203.5-green.svg)

Simple client api that handle working with the REST
api from Bambora.

Example
=======


Create a new bambora object:

    bambora = Bambora({
        "merchant_id": "[Merchant ID]",
        "url": "https://api.na.bambora.com",
        "codes": {
            "payment_passcode":  "payment passcode",
            "payment_profile_passcode": "payment profile passcode",
            "report_passcode": "report passcode",
        }
    })

Create a token with:


    token = bambora.tokens.create({
        'number': "4030000010001234",
        'expiry_month': "10",
        'expiry_year': "22",
        'cvd': "123"
    })

Create a new payment profile with:

    profile = bambora.profiles.create({
        'token': {
            'name': 'Test',
            'code': token.token
        },
        'language': 'fr'
    })

List all the cards for this profile:

    cards = profile.cards.list()


Create a payment with the currently created profile:

    payment = bambora.payments.create({
        "order_number": "Some order id",
        "amount": 20,
        "payment_method": "payment_profile",
        "payment_profile": {
            "customer_code": profile.customer_code,
            "card_id": cards[0].get_id()
        }
    })


Delete objects:

    trans1 = cards[0].delete()
    trans2 = profile.delete()
