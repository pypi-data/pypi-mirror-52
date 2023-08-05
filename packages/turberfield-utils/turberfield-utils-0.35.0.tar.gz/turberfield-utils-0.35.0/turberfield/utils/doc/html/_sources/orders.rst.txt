..  Titling
    ##++::==~~--''``

Business Rules
==============

Often in games or simulations, business rules are added incrementally as the
application evolves.

The :py:class:`Orders <turberfield.utils.orders.Orders>` class enables
you to register discrete snippets of code which you can call up in
the order they are defined in the class declaration.

This allows you to chain up callable rules without having to explicitly invoke
them one after the other.

Nothing is done behind your back. It's just that if you create a subclass of
:py:class:`Orders <turberfield.utils.orders.Orders>`, whichever methods
you register will be lined up sequentially for you to call them in the order
you wrote them. 

.. autoclass:: turberfield.utils.orders.Orders
   :members: register, methods
   :member-order: bysource
