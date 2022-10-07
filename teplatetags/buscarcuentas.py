from django import template
register= template.Library()


def buscaCuenta(ncuenta,arg):
    print("st")
    return("buscando")

register.filter('buscaCuenta', buscaCuenta)