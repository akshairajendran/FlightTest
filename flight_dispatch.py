__author__ = 'Akshai Rajendran'

from db_func import get_attr, get_allfid

#this function gets all recipients for a given flight and date
def all_recip(date,ident):
    #give this function a date as an epoch and an ident it will give you all receipients for that flight
    ids = get_allfid(date,ident)
    recips = [get_attr('recipient',id) for id in ids]
    return recips

#this function sends a message to a list of recipients