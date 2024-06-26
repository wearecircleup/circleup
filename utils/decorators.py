
import streamlit as st



"""
Este decorador valida que el usuario este accediendo al rol correcto, 
segun sean los atriutos de la instancia __set_name__()
"""
def guard(func):
    def wrapper(**kwargs):
        func()
    return wrapper
