#imported libraries
import numpy as np 
import random as r
import pandas as pd
import streamlit as st

class korvai_basic:
    
    #This is the list of talams the program works on currently. 
    #You can add more talams by adding name_of_talam: number of counts in one avarthanam
    TALAMS = {
        'adi':32,
        'adi2':64,
        'rupakam':12,
        'misra chaapu':14,
        'khanda chaapu':10,
        'jumpa':40
    }
    
    #All korvais generated in this program follow the template A A A B C B C B
    #The purvangam pattern is therefore A A A
    #Below is a dictionary for different A patterns based on the count between 5-9
    #To add more numeric options for A, change A_OPTIONS 
    A_OPTIONS = [5,6,7,8,9,10,16]
    #To add more varieties for a specific A, change PURVANGAMS values
    PURVANGAMS = {
        5: ['taka taang,, ', 'taki,ta, '],
        6: ['takadinatom, ', 'takitataang,, '],
        7: ['takadimi taang,, '],
        8: ['tatom, tadikitatom ','tadikitatom taang,, ','dit,takadinatom,'],
        9: ['takatom, tadikitatom '],
        10: ['taka,dina,taam,; '],
        16: ['taka,dina,taka,dina,taam,; ']
    }
    
    #The non-karvai part of the utarangams are B. They currently include patterns of numerican counts between 5-9
    #To add more numeric options for B, change B_OPTIONS
    B_OPTIONS = [5,6,7,8,9,12,15]
    #To add more varieties for a specific B, change UTARANGAMS values
    UTARANGAMS = {
        5: ['tadikitatom '],
        6: ['tadi,kitatom '],
        7: ['ta,di,kitatom ','tadi,kita,tom '],
        8: ['ta,di,,kitatom ','tatom, tadikitatom '],
        9: ['ta,di,ki,ta,tom ', 'ta,tom,tadikitatom '],
        12: ['takita takadimi tadikitatom '],
        15: ['tadikitatom tadikitatom tadikitatom ']
    }
    
    def __init__(self,talam,edam):
        self.talam = talam
        self.edam = edam
    
    #Given a number, this function calculates all possible B C B C B combinations
    #example: for 21, this function returns [[5, 3], [7, 0]]
    #which means 5 3 5 3 5 or 7 7 7 work as potential utarangams 
    def bc_combo(self, total):
        viable=[]
        for b in self.B_OPTIONS:
            if total<3*b:
                break
            remaining = total - 3*b 
            if remaining % 2 == 0:
                viable.append([b,int(remaining/2)])
        return viable 
    
    #Given a number, this function calculates all possible A A A B C B C B combinations using bc_combo as well
    #example: for 35, this function returns [[5, 6, 1], [6, 5, 1]]
    #which means 5 5 5 6 1 6 1 6 and 6 6 6 5 1 5 1 5 work as potential korvai structures
    def a_combo(self, total):
        viable=[]
        for a in self.A_OPTIONS:
            remaining = total - 3*a
            for bc in self.bc_combo(remaining):
                viable.append([a,bc[0],bc[1]])
        return viable
    
    #This function uses the talam and edam specified during initialization to calculate all combinations of korvais
    #using a_combo and b_combo
    #It also calculates the optimal number of avarthanams needed to create a korvai within the limits of A & B bounds provided
    #This can be changed in the while loop (right now the function requires a minimum total of 90 beats for the entire korvai)
    def korvai(self):
        base = self.TALAMS[self.talam]
        n=1
        tentative=base*n+self.edam
        while tentative<=90:
            n=n+1
            tentative=base*n+self.edam
        for i in np.arange(3):
            if tentative%3!=0:
                n=n+1
                tentative=base*n+self.edam
        return self.a_combo(tentative/3)
        #try:
            #return self.a_combo(tentative/3)
        #except:
            #return -1
    
    #This function uses the korvai function to collect all possible korvai options
    #For each korvai option, it randomly a selects a purvangam konokol and utarangam konokol 
    #This provides an example konokol for how an AAABCBCB korvai can be structured given a talam and edam 
    def final_korvai(self):
        korvai_options = self.korvai()
        korvai_list=[]
        #if korvai_options == -1:
            #return('impossible to make a korvai, maybe try singing an edam to edam korvai here')
        for k in korvai_options:
            a,b,c=k
            A = r.choice(self.PURVANGAMS[a])
            B = r.choice(self.UTARANGAMS[b])
            if c == 0:
                C=''
            elif c == 1:
                C=','
            else:
                C = 'taam' + (','*(c-1))
            print('pattern: ',a,a,a,b,c,b,c,b)
            print(3*A,B,C,B,C,B)
            print(3*A,B,C,B,C,B)
            print(3*A,B,C,B,C,B)
            print()
            #returns korvai list as a dataframe here
            str_korvai=3*A+B+C+B+C+B
            korvai_list.append(str_korvai)
        return pd.DataFrame(korvai_list,columns={'korvai'})

#The main method takes in a talam and edam (watch out for spelling of the talam LOL) and returns 1+ possible korvais
def main():
    
    st.title("Welcome to Korvai Calculator!")
    talam = st.sidebar.selectbox(
        "Select the Talam:",
        ["adi", "adi2", "rupakam", "misra chaapu", "khanda chaapu", "jumpa"])
    edam = st.sidebar.slider('What is the Edam?', -10, 20, 1)
    st.write('Your Talam is ', talam)
    st.write('Your Edam is ', edam)
    my_korvai = korvai_basic(talam,edam)
    df = my_korvai.final_korvai()
    st.table(df)
    st.balloons()

if __name__ == "__main__":
    main()
