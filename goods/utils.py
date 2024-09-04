from django.db.models import Q

from goods.models import Product


def q_search(query):
    """Q products search based on name & description"""
    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    return Product.objects.filter(description__search=query)

    # keywords = [word for word in query.split() if len(word) > 2]
    #
    # q_objects = Q()
    #
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
    #
    #     return Product.objects.filter(q_objects)
