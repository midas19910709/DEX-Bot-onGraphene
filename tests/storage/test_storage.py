import logging

log = logging.getLogger("dexbot")
log.setLevel(logging.DEBUG)


def test_fetch_orders(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    storage.save_order(order)
    fetched = storage.fetch_orders()
    # Return value is dict {'id': 'order'}
    assert fetched[order['id']] == order


def test_fetch_orders_extended(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    text = 'foo bar'
    storage.save_order_extended(order, virtual=True, custom=text)

    fetched = storage.fetch_orders_extended(only_real=True)
    assert len(fetched) == 0
    fetched = storage.fetch_orders_extended(only_virtual=True)
    assert len(fetched) == 1
    fetched = storage.fetch_orders_extended(custom=text)
    assert len(fetched) == 1
    fetched = storage.fetch_orders_extended(return_ids_only=True)
    assert fetched == ['111']

    fetched = storage.fetch_orders_extended()
    assert isinstance(fetched, list)
    result = fetched[0]
    assert result['custom'] == 'foo bar'
    assert result['virtual'] is True
    assert result['order'] == order
