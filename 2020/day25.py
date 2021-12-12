import template
import copy
import regex as re
import math 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from time import time, strftime, localtime



# --- #
def do_transform_via_loop(subject, loop_size):
    v = 1
    for i in range(loop_size):
        v = v * subject
        v = v % 20201227
    return v

def do_transform_step(subject, last_val):
    v = last_val
    v = v * subject
    v = v % 20201227
    return v
    
def do_transform(subject, loop_size):
    x = (subject ** loop_size) % 20201227
    return x

def part1():
    card_pk = 8987316
    door_pk = 14681524

    card_loops = None
    door_loops = None
    i = 0
    last_val = 1
    while card_loops is None or door_loops is None:
        i += 1
        trans_val = do_transform_step(7, last_val)
        # print("Loop", i, trans_val)
        if trans_val == card_pk:
            print("Got card loops:", i)
            card_loops = i
        if trans_val == door_pk:
            print("Got door loops:", i)
            door_loops = i
        last_val = trans_val

    print(card_loops, door_loops)
    
    start = time()
    enc_key1 = do_transform_via_loop(door_pk, card_loops)
    end = time()
    print("Loop: Executed in %s seconds"%template.secondsToStr(end - start))
    
    start = time()
    enc_key2 = do_transform_via_loop(card_pk, door_loops)
    end = time()
    print("Exponent: Executed in %s seconds"%template.secondsToStr(end - start))
    

    print("Keys: ", enc_key1, enc_key2, enc_key1 == enc_key2)
    
    return enc_key1
    
def part2():
    return 1
    
# --- #

if __name__ == "__main__":
    template.funWrapper(part1, "Part 1")
    template.funWrapper(part2, "Part 2")

    
        