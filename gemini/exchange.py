class OpenedTrade:
    """
    Open trades main class
    """
    def __init__(self, order_type, date):
        self.order_type = order_type
        self.date = date

    def __str__(self):
        return "{0}\n{1}".format(self.order_type, self.date)


class ClosedTrade(OpenedTrade):
    """
    Closed trade class
    """
    def __init__(self, order_type, date, shares, entry, exit):
        super().__init__(order_type, date)
        self.shares = float(shares)
        self.entry = float(entry)
        self.exit = float(exit)

    def __str__(self):
        return "{0}\n{1}\n{2}\n{3}\n{4}".format(self.order_type, self.date,
                                                self.shares, self.entry,
                                                self.exit)


class Position:
    """
    Position main class
    """
    def __init__(self, number, entry_price, shares, exit_price=0, stop_loss=0):
        self.number = number
        self.order_type = "None"
        self.entry_price = float(entry_price)
        self.shares = float(shares)
        self.exit_price = float(exit_price)
        self.stop_loss = float(stop_loss)

    def show(self):
        """
        Print position info
        :return:
        """
        print("No. {0}".format(self.number))
        print("Type:   {0}".format(self.order_type))
        print("Entry:  {0}".format(self.entry_price))
        print("Shares: {0}".format(self.shares))
        print("Exit:   {0}".format(self.exit_price))
        print("Stop:   {0}\n".format(self.stop_loss))


class LongPosition(Position):
    """
    Long position class
    """
    def __init__(self, number, entry_price, shares, exit_price=0, stop_loss=0):
        super().__init__(number, entry_price, shares, exit_price, stop_loss)
        self.order_type = 'Long'

    def close(self, percent, current_price):
        """
        ??? don't understand ???
            - return results of deal to Account.initial_capital/buying_power?
        :param percent:
        :param current_price:
        :return:
        """
        shares = self.shares
        self.shares *= 1.0 - percent
        return shares * percent * current_price


class ShortPosition(Position):
    """
    Short position class
    """
    def __init__(self, number, entry_price, shares, exit_price=0, stop_loss=0):
        super().__init__(number, entry_price, shares, exit_price, stop_loss)
        self.order_type = 'Short'

    def close(self, percent, current_price):
        """
        ??? don't understand ???
            - return results of deal to Account.initial_capital/buying_power?
        :param percent:
        :param current_price:
        :return:
        """
        entry = self.shares * percent * self.entry_price
        exit = self.shares * percent * current_price
        self.shares *= 1.0 - percent
        if entry - exit + entry <= 0:
            return 0
        else:
            return entry - exit + entry


class Account:
    """
    Main account class
    Store settings and trades data
    """
    def __init__(self, initial_capital):
        self.initial_capital = float(initial_capital)
        self.buying_power = float(initial_capital)
        self.number = 0
        self.date = None
        self.equity = []
        self.positions = []
        self.opened_trades = []
        self.closed_trades = []

    def enter_position(self, order_type, entry_capital, entry_price, exit_price=0,
                       stop_loss=0):
        """
        Open position
        :param order_type:
        :param entry_capital:
        :param entry_price:
        :param exit_price:
        :param stop_loss:
        :return:
        """

        entry_capital = float(entry_capital)
        if entry_capital < 0:
            raise ValueError("Error: Entry capital must be positive")
        elif entry_price < 0:
            raise ValueError("Error: Entry price cannot be negative.")
        elif self.buying_power < entry_capital:
            raise ValueError("Error: Not enough buying power to enter position")
        else:
            self.buying_power -= entry_capital
            shares = entry_capital / entry_price
            if order_type == 'Long':
                self.positions.append(
                    LongPosition(self.number, entry_price, shares, exit_price,
                                 stop_loss))
            elif order_type == 'Short':
                self.positions.append(
                    ShortPosition(self.number, entry_price, shares, exit_price,
                                  stop_loss))
            else:
                raise TypeError("Error: Invalid position type.")

            self.opened_trades.append(OpenedTrade(order_type, self.date))
            self.number += 1

    def close_position(self, position, percent, current_price):
        """
        close position
        :param position:
        :param percent:
        :param current_price:
        :return:
        """
        if percent > 1 or percent < 0:
            raise ValueError("Error: Percent must range between 0-1.")  # FIXME: why just between 0-1?
        elif current_price < 0:                                         # because 0.25 = 25% ?
            raise ValueError("Error: Current price cannot be negative.")
        else:
            self.closed_trades.append(
                ClosedTrade(position.order_type, self.date, position.shares * percent,
                            position.entry_price, current_price))
            self.buying_power += position.close(percent, current_price)

    def purge_positions(self):
        """
        Delete positions without shares?
        :return:
        """
        self.positions = [p for p in self.positions if p.shares > 0]

    def show_positions(self):
        """
        Show open position info
        :return:
        """
        for p in self.positions:
            p.show()

    def total_value(self, current_price):
        """
        Something strange here

        :param current_price:
        :return:
        """
        # FIXME Try to understand what happend here
        """
        temporary = copy.deepcopy(self)
        for position in temporary.positions:
            temporary.close_position(position, 1.0, current_price)
        return temporary.buying_power
        # """
        in_pos = sum([p.shares * current_price for p in self.positions])
        return self.buying_power + in_pos
