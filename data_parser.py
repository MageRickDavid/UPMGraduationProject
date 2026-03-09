# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    data_parser.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/07 06:03:50 by rortiz            #+#    #+#              #
#    Updated: 2026/03/10 08:19:58 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd

def program(station: str):
    table = pd.read_csv("listado-estaciones-cercanias-madrid.csv", sep=",",encoding="latin1",
                        usecols=["CODIGO", "DESCRIPCION", "LATITUD", "LONGITUD", "LINES"])
    print(table.head())
    output = table[table["DESCRIPCION"].str.contains(station, case=False)]
    print(output)

def save_data():
    table = pd.read_csv("listado-estaciones-cercanias-madrid.csv", sep=",",encoding="latin1",
                        usecols=["CODIGO", "DESCRIPCION", "LATITUD", "LONGITUD", "LINES"])
    table.to_csv("data.csv", index=False)
    
def main():
    while True:
        station = input("station: ").strip()

        if station == "exit":
            print("Goodbye")
            break
        if station == "save":
            save_data()
            break
        try:
            program(station)
        except Exception as e:
            print("The program failed:" , e)
            break
        

if __name__ == "__main__":
    main()

    
