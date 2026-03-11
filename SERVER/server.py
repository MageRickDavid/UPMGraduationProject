# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 21:59:35 by rortiz            #+#    #+#              #
#    Updated: 2026/03/11 23:16:25 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import FastAPI
from helper import *

app = FastAPI()

@app.get("/stations/{name}")
def get_station(name: str):
    stations = find_station(name)
    return {"query": name, "results": stations}

@app.get("/linesFromStation/{name}")
def get_lines_from_station_name(name):
    lines = get_lines(name)
    return {"query": name, "results": lines}
