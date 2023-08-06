import operator
from collections import defaultdict


class UnbalancedRequest(Exception):
    pass


def settle(balances):
    debiters, crediters = order_balance(balances)
    check_balance(debiters, crediters)
    return reduce_balance(debiters, crediters)


def check_balance(debiters, crediters):
    def _sum(balance):
        return sum([abs(v) for _, v in balance])

    sum_debiters = _sum(debiters)
    sum_crediters = _sum(crediters)

    if not sum_crediters == sum_debiters:
        raise UnbalancedRequest(
            f"Unsolvable : debiters (-{sum_debiters}) and crediters "
            f"(+{sum_crediters}) are unbalanced."
        )


def order_balance(balances):
    balances_dict = defaultdict(float)

    for _id, balance in balances:
        balances_dict[_id] += balance

    crediters = list()
    debiters = list()
    for _id, balance in balances_dict.items():
        if float(balance) > 0:
            crediters.append((_id, balance))
        else:
            debiters.append((_id, balance))

    return debiters, crediters


def reduce_balance(crediters, debiters, results=None):
    if len(crediters) == 0 or len(debiters) == 0:
        return results

    if results is None:
        results = []

    crediters.sort(key=operator.itemgetter(1))
    debiters.sort(key=operator.itemgetter(1), reverse=True)

    debiter, debiter_balance = crediters.pop()
    crediter, crediter_balance = debiters.pop()

    if abs(debiter_balance) > abs(crediter_balance):
        amount = abs(crediter_balance)
    else:
        amount = abs(debiter_balance)
    new_results = results[:]
    new_results.append((debiter, amount, crediter))

    new_debiter_balance = debiter_balance + amount
    if new_debiter_balance < 0:
        crediters.append((debiter, new_debiter_balance))
        crediters.sort(key=operator.itemgetter(1))

    new_crediter_balance = crediter_balance - amount
    if new_crediter_balance > 0:
        debiters.append((crediter, new_crediter_balance))
        debiters.sort(key=operator.itemgetter(1), reverse=True)

    return reduce_balance(crediters, debiters, new_results)
