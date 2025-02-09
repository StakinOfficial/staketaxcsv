from staketaxcsv.common.make_tx import make_transfer_in_tx, make_transfer_out_tx, make_unknown_tx
from staketaxcsv.luna1.col5.actions.complete_transfer_wrapped import handle_action_complete_transfer_wrapped
from staketaxcsv.luna1.col5.contracts.config import CONTRACTS
from staketaxcsv.luna1 import util_terra

def handle_wormhole(elem, txinfo):
    txinfo.comment += "bridge wormhole"

    for msg in txinfo.msgs:
        transfers_in, transfers_out = msg.transfers

        # Check native coins
        if len(transfers_in) == 1 and len(transfers_out) == 0:
            amount, currency = transfers_in[0]
            row = make_transfer_in_tx(txinfo, amount, currency)
            return [row]
        elif len(transfers_out) == 1 and len(transfers_in) == 0:
            amount, currency = transfers_out[0]
            row = make_transfer_out_tx(txinfo, amount, currency)
            return [row]

        # Check other coins
        for action in msg.actions:
            if "action" in action and action["action"] == "complete_transfer_wrapped":
                rows = handle_action_complete_transfer_wrapped(txinfo, action)
                return rows
            elif "action" in action and action["action"] == "burn_from":
                amount_string = action["amount"]
                currency_address = action["contract_address"]

                currency = util_terra._lookup_address(currency_address, "")
                amount = util_terra._float_amount(amount_string, currency)
                row = make_transfer_out_tx(txinfo, amount, currency)
                return [row]

    row = make_unknown_tx(txinfo)
    return [row]


# Wormhole Contracts
CONTRACTS["terra10nmmwe8r3g99a9newtqa7a75xfgs2e8z87r2sf"] = handle_wormhole
