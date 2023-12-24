def orders_improve_data_output_view(orders):
    res = []
    for order in orders:
        item = {
            "id_product": order.id_product,
            "login_user": order.login_user,
            "final_price": order.final_price,
            "trans_datetime": order.trans_datetime.strftime('%Y-%m-%d'),
        }
        res.append(item)
    return res
