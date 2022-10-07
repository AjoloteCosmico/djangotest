from django import template
register= template.Library()

@register.simple_tag
def buscaCuenta(ncuenta):
    print(" el numero es: "+ncuenta)
    return("buscando")

#register.filter('buscaCuenta', buscaCuenta)