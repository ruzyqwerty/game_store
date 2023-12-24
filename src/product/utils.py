def products_improve_data_output_view(products):
    res = []
    for product in products:
        item = {
            "id_product": product.id_product,
            "title": product.title,
            "creation_date": product.creation_date.strftime('%Y-%m-%d'),
            "price": product.price,
            "genre": product.genre,
            "vers": product.vers,
            "main_product": product.main_product,
            "login_user": product.login_user,
        }
        res.append(item)
    return res
