# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    data_parser.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/07 06:03:50 by rortiz            #+#    #+#              #
#    Updated: 2026/03/07 07:44:34 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd

def program(station: str):
    table = pd.read_csv("estaciones.csv", sep=";",encoding="latin1",
                        usecols=["CODIGO", "DESCRIPCION", "LATITUD", "LONGITUD", "PROVINCIA"])
    table = table[(table["PROVINCIA"] == "MADRID") | (table["PROVINCIA"] == "GUADALAJARA")  ]
    print(table.head())
    output = table[table["DESCRIPCION"].str.contains(station)]
    print(output)

def main():
    while True:
        station = input("station: ").strip()

        if station == "exit":
            print("Goodbye")
            break
        try:
            program(station)
        except Exception as e:
            print("The program failed:" , e)
            break
        

if __name__ == "__main__":
    main()

    
