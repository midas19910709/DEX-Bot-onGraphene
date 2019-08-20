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


def test_clear_orders(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    storage.save_order(order)
    storage.clear_orders()
    fetched = storage.fetch_orders()
    assert fetched is None


def test_clear_orders_extended(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    storage.save_order_extended(order, virtual=True)
    storage.clear_orders_extended(only_virtual=True)
    fetched = storage.fetch_orders_extended()
    assert fetched == []

    storage.save_order_extended(order, custom='foo')
    storage.clear_orders_extended(custom='foo')
    fetched = storage.fetch_orders_extended()
    assert fetched == []


def test_remove_order(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    storage.save_order(order)
    storage.remove_order(order)
    assert storage.fetch_orders() is None


def test_remove_order_by_id(storage):
    order = {'id': '111', 'base': '10 CNY', 'quote': '1 BTS'}
    storage.save_order(order)
    storage.remove_order(order['id'])
    assert storage.fetch_orders() is None
