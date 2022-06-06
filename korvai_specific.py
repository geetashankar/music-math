#imported libraries
import numpy as np 
import random as r
import pandas as pd
import streamlit as st

class korvai_specific:
    
    UTARANGAMS = {
        15: 'tadinginatom tadinginatom tadinginatom',
        17: 'tadinginatom, tadinginatom, tadinginatom',
        18: 'tadin,ginatom tadin,ginatom tadin,ginatom',
        19: 'tadinginatom taam, tadinginatom taam, tadinginatom',
        20: 'tadin,ginatom, tadin,ginatom, tadin,ginatom',
        21: 'ta,din,ginatom ta,din,ginatom ta,din,ginatom',
        22: 'tadin,ginatom taam, tadin,ginatom taam, tadin,ginatom',
        23: 'ta,din,ginatom, ta,din,ginatom, ta,din,ginatom',
        24: 'tatom,tadinginatom tatom,tadinginatom tatom,tadinginatom',
        25: 'ta,din,ginatom taam, ta,din,ginatom taam, ta,din,ginatom',
        26: 'tatom,tadinginatom, tatom,tadinginatom, tatom,tadinginatom',
        27: 'ta,din,gi,na,tom ta,din,gi,na,tom ta,din,gi,na,tom'
    }
    
    TALAMS = {
        'adi':32,
        'adi2':64,
        'rupakam':12,
        'misra chaapu':14,
        'khanda chaapu':10,
        'jumpa':40
    }
    
    PURVANGAM1 = ['tha,ki,ta,thakadina','tha,dhi,thakadina','dhi,thakadina','thakadina']
    PURVANGAM2 = ['tha,ka,di,na,thakadina','tha,ki,ta,thakadina','tha,dhi,thakadina','dhi,thakadina']
    
    KARVAIS = np.arange(4,0,-1)
    KARVAI_KONOKOL = {
        4:'thaam,;',
        3:'thaang,,',
        2:'thaam,',
        1:','
    }
    
    VIABLE_COUNTS = np.concatenate(([47],np.arange(49,80)))
    
    
    def __init__(self,talam,edam):
        self.talam = talam
        self.edam = edam
    
    def abc_combo(self,total):
        viable=[]
        for k in self.KARVAIS:
            #print(k)
            remaining1 = total - 28 - 4*k
            #print(remaining1)
            if remaining1 in self.UTARANGAMS.keys():
                    viable.append([28,k,remaining1])
            remaining2=total - 36 - 4*k
            if remaining2 in self.UTARANGAMS.keys():
                    viable.append([36,k,remaining2])
        return viable

    def korvai(self):
        talam = self.TALAMS[self.talam]
        korvai_options=[]
        final_list=[]
        for i in np.arange(20):
            num=talam*i+self.edam
            if num%3==0:
                if num/3 in self.VIABLE_COUNTS:
                    korvai_options.append(self.abc_combo(int(num/3)))
        for i in korvai_options:
            for j in i:
                final_list.append(j)
        return final_list

    def final_korvai(self):
        final_list = self.korvai()
        korvai_list=[]
        for i in final_list:
            korvai_str=''
            print('Repeat pattern 3 times: \n')
            korvai_str=''
            if i[0]==28:
                for p in self.PURVANGAM1:
                    print(p,self.KARVAI_KONOKOL[i[1]])
                    korvai_str=korvai_str+p+self.KARVAI_KONOKOL[i[1]]
                print(self.UTARANGAMS[i[2]],'\n','__________________','\n')
                korvai_str=korvai_str+self.UTARANGAMS[i[2]]

            elif i[0]==36:
                for p in self.PURVANGAM2:
                    print(p,self.KARVAI_KONOKOL[i[1]])
                    korvai_str=korvai_str+p+self.KARVAI_KONOKOL[i[1]]
                print(self.UTARANGAMS[i[2]],'\n','__________________','\n')
                korvai_str=korvai_str+self.UTARANGAMS[i[2]]
            korvai_list.append(korvai_str)
        if len(pd.DataFrame(korvai_list,columns={'korvai'}))==0:
            return 'impossible to make a korvai, maybe try singing an edam to edam korvai here'
        else:
            return pd.DataFrame(korvai_list,columns={'korvai'})

#The main method takes in a talam and edam (watch out for spelling of the talam LOL) and returns 1+ possible korvais
def main():

    st.title("Welcome to my second Korvai Calculator!")
    talam = st.sidebar.selectbox(
        "Select the Talam:",
        ["adi", "adi2", "rupakam", "misra chaapu", "khanda chaapu", "jumpa"])
    edam = st.sidebar.slider('What is the Edam?', -10, 20, 1)
    st.write('Your Talam is ', talam)
    st.write('Your Edam is ', edam)
    my_korvai = korvai_specific(talam,edam)
    df = my_korvai.final_korvai()
    st.table(df)

if __name__ == "__main__":
    main()