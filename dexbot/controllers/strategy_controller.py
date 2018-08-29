from dexbot.qt_queue.idle_queue import idle_add
from dexbot.views.errors import gui_error
from dexbot.strategies.staggered_orders import Strategy as StaggeredOrdersStrategy

from bitshares.market import Market
from bitshares.asset import AssetDoesNotExistsException
from PyQt5 import QtWidgets


class StrategyController:
    """ Parent controller for strategies that don't have a custom controller
    """

    def __init__(self, view, configure, worker_controller, worker_data):
        self.view = view
        self.configure = configure
        self.worker_controller = worker_controller

        self.set_values(configure, worker_data)

    def validation_errors(self):
        return []

    def set_values(self, configure, worker_config):
        for option in configure:
            if worker_config and worker_config.get(option.key) is not None:
                value = worker_config[option.key]
            else:
                value = option.default

            element = self.elements.get(option.key)
            if element is None:
                continue

            if option.type in ('int', 'float', 'string'):
                element.setValue(value)
            if option.type == 'bool':
                if value:
                    element.setChecked(True)
                else:
                    element.setChecked(False)
            if option.type == 'choice':
                # Fill the combobox
                for tag, label in option.extra:
                    element.addItem(label, tag)
                # Set the value
                index = element.findData(value)
                element.setCurrentIndex(index)

    @property
    def values(self):
        data = {}
        for key, element in self.elements.items():
            class_name = element.__class__.__name__
            if class_name in ('QDoubleSpinBox', 'QSpinBox', 'QLineEdit', 'QSlider'):
                data[key] = element.value()
            elif class_name == 'QCheckBox':
                data[key] = element.isChecked()
            elif class_name == 'QComboBox':
                data[key] = element.currentData()
        return data

    @property
    def elements(self):
        """ Use ConfigElements of the strategy to find the input elements
        """
        elements = {}
        types = (
            QtWidgets.QDoubleSpinBox,
            QtWidgets.QSpinBox,
            QtWidgets.QLineEdit,
            QtWidgets.QCheckBox,
            QtWidgets.QComboBox,
            QtWidgets.QSlider
        )

        for option in self.configure:
            element_name = ''.join([option.key, '_input'])
            element = self.view.findChild(types, element_name)
            if element is not None:
                elements[option.key] = element
        return elements


class RelativeOrdersController(StrategyController):

    def __init__(self, view, configure, worker_controller, worker_data):
        self.view = view
        self.configure = configure
        self.worker_controller = worker_controller

        # Refresh center price market label
        self.onchange_asset_labels()

        # Refresh center price market label every time the text changes is base or quote asset input fields
        worker_controller.view.base_asset_input.textChanged.connect(self.onchange_asset_labels)
        worker_controller.view.quote_asset_input.textChanged.connect(self.onchange_asset_labels)

        self.view.strategy_widget.relative_order_size_input.toggled.connect(
            self.onchange_relative_order_size_input
        )
        self.view.strategy_widget.center_price_dynamic_input.toggled.connect(
            self.onchange_center_price_dynamic_input
        )
        self.view.strategy_widget.manual_offset_input.valueChanged.connect(
            self.onchange_manual_offset_input
        )

        # QSlider uses (int) values and manual_offset is stored as (float) with 0.1 precision.
        # This reverts it so QSlider can handle the number, when fetching from config.
        if worker_data:
            worker_data['manual_offset'] = worker_data['manual_offset'] * 10

        # Do this after the event connecting
        super().__init__(view, configure, worker_controller, worker_data)

        if not self.view.strategy_widget.center_price_dynamic_input.isChecked():
            self.view.strategy_widget.center_price_input.setDisabled(False)

    @property
    def values(self):
        # This turns the int value of manual_offset from QSlider to float with desired precision.
        values = super().values
        values['manual_offset'] = values['manual_offset'] / 10
        return values

    def onchange_manual_offset_input(self):
        value = self.view.strategy_widget.manual_offset_input.value() / 10
        text = "{}%".format(value)
        self.view.strategy_widget.manual_offset_amount_label.setText(text)

    def onchange_relative_order_size_input(self, checked):
        if checked:
            self.order_size_input_to_relative()
        else:
            self.order_size_input_to_static()

    def onchange_center_price_dynamic_input(self, checked):
        if checked:
            self.view.strategy_widget.center_price_input.setDisabled(True)
        else:
            self.view.strategy_widget.center_price_input.setDisabled(False)

    def onchange_asset_labels(self):
        base_symbol = self.worker_controller.view.base_asset_input.text()
        quote_symbol = self.worker_controller.view.quote_asset_input.text()

        if quote_symbol:
            self.set_amount_asset_label(quote_symbol)
        else:
            self.set_amount_asset_label('')

        if base_symbol and quote_symbol:
            text = '{} / {}'.format(base_symbol, quote_symbol)
            self.set_center_price_market_label(text)
        else:
            self.set_center_price_market_label('')

    def order_size_input_to_relative(self):
        self.view.strategy_widget.amount_input.setSuffix('%')
        self.view.strategy_widget.amount_input.setDecimals(2)
        self.view.strategy_widget.amount_input.setMaximum(100.00)
        self.view.strategy_widget.amount_input.setMinimumWidth(170)

    def order_size_input_to_static(self):
        self.view.strategy_widget.amount_input.setSuffix('')
        self.view.strategy_widget.amount_input.setDecimals(8)
        self.view.strategy_widget.amount_input.setMaximum(1000000000.000000)

    def set_center_price_market_label(self, text):
        self.view.strategy_widget.center_price_market_label.setText(text)

    def set_amount_asset_label(self, text):
        self.view.strategy_widget.amount_input_asset_label.setText(text)

    def validation_errors(self):
        error_texts = []
        if not self.view.strategy_widget.amount_input.value():
            error_texts.append("Order size can't be 0")
        if not self.view.strategy_widget.spread_input.value():
            error_texts.append("Spread can't be 0")
        return error_texts


class StaggeredOrdersController(StrategyController):

    def __init__(self, view, configure, worker_controller, worker_data):
        self.view = view
        self.configure = configure
        self.worker_controller = worker_controller

        worker_controller.view.base_asset_input.textChanged.connect(lambda: self.on_value_change())
        worker_controller.view.quote_asset_input.textChanged.connect(lambda: self.on_value_change())
        widget = self.view.strategy_widget
        widget.amount_input.valueChanged.connect(lambda: self.on_value_change())
        widget.spread_input.valueChanged.connect(lambda: self.on_value_change())
        widget.increment_input.valueChanged.connect(lambda: self.on_value_change())
        widget.center_price_dynamic_input.stateChanged.connect(lambda: self.on_value_change())
        widget.center_price_input.valueChanged.connect(lambda: self.on_value_change())
        widget.lower_bound_input.valueChanged.connect(lambda: self.on_value_change())
        widget.upper_bound_input.valueChanged.connect(lambda: self.on_value_change())
        self.on_value_change()

        # Do this after the event connecting
        super().__init__(view, configure, worker_controller, worker_data)

        if not self.view.strategy_widget.center_price_dynamic_input.isChecked():
            self.view.strategy_widget.center_price_input.setDisabled(False)

    @gui_error
    def on_value_change(self):
        base_asset = self.worker_controller.view.base_asset_input.text()
        quote_asset = self.worker_controller.view.quote_asset_input.text()
        try:
            market = Market('{}:{}'.format(quote_asset, base_asset))
        except AssetDoesNotExistsException:
            idle_add(self.set_required_base, 'N/A')
            idle_add(self.set_required_quote, 'N/A')
            return

        amount = self.view.strategy_widget.amount_input.value()
        spread = self.view.strategy_widget.spread_input.value() / 100
        increment = self.view.strategy_widget.increment_input.value() / 100
        lower_bound = self.view.strategy_widget.lower_bound_input.value()
        upper_bound = self.view.strategy_widget.upper_bound_input.value()
        if self.view.strategy_widget.center_price_dynamic_input.isChecked():
            center_price = None
        else:
            center_price = self.view.strategy_widget.center_price_input.value()

        if not (market or amount or spread or increment or lower_bound or upper_bound):
            idle_add(self.set_required_base, 'N/A')
            idle_add(self.set_required_quote, 'N/A')
            return

        strategy = StaggeredOrdersStrategy
        result = strategy.get_required_assets(market, amount, spread, increment, center_price, lower_bound, upper_bound)
        if not result:
            idle_add(self.set_required_base, 'N/A')
            idle_add(self.set_required_quote, 'N/A')
            return

        base, quote = result
        text = '{:.8f} {}'.format(base, base_asset)
        idle_add(self.set_required_base, text)
        text = '{:.8f} {}'.format(quote, quote_asset)
        idle_add(self.set_required_quote, text)

    def set_required_base(self, text):
        self.view.strategy_widget.required_base_text.setText(text)

    def set_required_quote(self, text):
        self.view.strategy_widget.required_quote_text.setText(text)

    def validation_errors(self):
        error_texts = []
        if not self.view.strategy_widget.amount_input.value():
            error_texts.append("Order size can't be 0")
        if not self.view.strategy_widget.spread_input.value():
            error_texts.append("Spread can't be 0")
        if not self.view.strategy_widget.increment_input.value():
            error_texts.append("Increment can't be 0")
        if not self.view.strategy_widget.lower_bound_input.value():
            error_texts.append("Lower bound can't be 0")
        return error_texts
