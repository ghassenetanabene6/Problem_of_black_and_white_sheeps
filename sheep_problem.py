"""

Python script to solve the problem of black and white sheeps.

****************************************************************************************************************************************
                                            Ghassene Tanabene
                                        ghassene.tanabene@gmail.com
                                              November 2021
****************************************************************************************************************************************

Usage :

    $python sheep_problem.py --nb_B number_of_black_sheeps --nb_W number_of_white_sheeps


My algorithm :
----------------------------------------------------------------------------------------------------------------------------------------
"W"="White", "B"="Black", "S"="Empty Space", "C"="Color W or B", "Not_C"="the other color"

We start first by moving "W"

*If the 2 <= space_index <= len(List_of_sheeps)-2
    - if ("C","S","C") => Jump "Not_C" if it is possible else move "C" 
    - else => ("C","S","Not_C") : move the sheep having the color same to the color in the memory (last operation) if it is possible
*Else : 
- The 4 cases where "S" appears in the position {0,1,len(L)-1,len(L)-2} are treated separately
    [S,...], [C,S,...], [...,S,C], [...,S]
----------------------------------------------------------------------------------------------------------------------------------------

"""




import argparse

def move(color,L,space_index):
    '''
        Moving one single sheep : permutation of (S,W) or (B,S).

        args :
            color : sheep color "W" or "B"
            L : List of sheeps
            space_index : the index of "S" in L
        
    '''
    if color == "W":
        L[space_index],L[space_index+1]=L[space_index+1],L[space_index]
    else :
        L[space_index],L[space_index-1]=L[space_index-1],L[space_index]
        

def jump(color,L,space_index):
    
    '''
        Function that allows a sheep to jump over another sheep

        args :
            color : sheep color "W" or "B"
            L : List of sheeps
            space_index : the index of "S" in L
        
    '''
    if color == "W":
        L[space_index],L[space_index+2]=L[space_index+2],L[space_index]
    else :
        L[space_index],L[space_index-2]=L[space_index-2],L[space_index]

def same_color(L,space_index):
    '''
        Function that checks whether two sheeps to the left and to the right of the empty space have the same colors or not.

        args :
            L : List of sheeps
            space_index : the index of "S" in L
        
    '''
    return(L[space_index-1]==L[space_index+1])

def can_jump(color,L,space_index):
    '''
        Function that checks if a sheep can jump.
        args :
            color : sheep color "W" or "B"
            L : List of sheeps
            space_index : the index of "S" in L
    '''
    if color==L[space_index+2]=="W" and L[space_index+1]=="B":
        return(True)
    elif color==L[space_index-2]=="B" and L[space_index-1]=="W":
        return(True)
    return(False)

def main():
    
    args = parse_arguments()
    nb_B=args.nb_B #defaut_value = 4
    nb_W=args.nb_W #defaut_value = 3
    if (nb_B==0 or nb_W==0):
        print("Please check if the nb_B>0 and nb_W>0")
        return (0)
    Black=["B" for i in range(nb_B)]
    White=["W" for i in range(nb_W)]
    L=Black+["S"]+White
    Final_List=White+["S"]+Black  #Final Result
    space_index=L.index("S")
    
    print("Step 0 = ",L)
    move("W",L,space_index)
    memory="W" #variable containing the sheep color of the last step 
    print("Step 1 = ",L)
    i=2 #the step index
    
    while L!=Final_List :
        space_index=L.index("S")

        # The 4 cases where "S" appears in the position {0,1,len(L)-1,len(L)-2} are treated separately
        
        if space_index==0:
            if (L[space_index+1]=="W"):
                move("W",L,space_index)
                memory="W"
            elif(L[space_index+1]=="B" and L[space_index+2]=="W"):
                jump("W",L,space_index)
                memory="W"
                
            else:
                print("BLOCK !")
                pass
        
        elif space_index==1:

            if L[space_index-1]==L[space_index+1]=="W" :
                move("W",L,space_index) #because B can't move backword
                memory="W"
            elif L[space_index-1]==L[space_index+1]=="B" :
                if L[space_index+2]=="W":
                    jump("W",L,space_index)
                    memory="W"
                else:
                    move("B",L,space_index)
                    memory="B"
            elif L[space_index+1]=="B" and L[space_index-1]==L[space_index+2]=="W":
                    jump("W",L,space_index)
                    memory="W"
            elif L[space_index-1]=="B" and memory =="B":
                    move(memory,L,space_index)
            elif L[space_index+1]=="W" and memory =="W":
                    move(memory,L,space_index)
            else :
                print("BLOC : [W,S,B,B,..]!")
                pass
                
            
        elif space_index==len(L)-1:
            if (L[space_index-1]=="B"):
                move("B",L,space_index)
                memory="B"
            elif(L[space_index-1]=="W" and L[space_index-2]=="B"):
                jump("B",L,space_index)
                memory="B"
                
            else:
                print("BLOCK : [...,W,W,S,B]!")
                pass
                
           
        elif space_index==len(L)-2 :
            if L[space_index-1]==L[space_index+1]=="B" :
                move("B",L,space_index) #because W can't move backword
                memory="B"
            elif L[space_index-1]==L[space_index+1]=="W" :
                if L[-4]=="B":
                    jump("B",L,space_index)
                    memory="B"
                else:
                    move("W",L,space_index) 
                    memory="W"
            elif L[-3]=="W" and L[-1]==L[-4]=="B":
                jump("B",L,space_index)
                memory="B"
                
            elif L[space_index-1]=="B" and memory =="B":
                move(memory,L,space_index)
            elif L[space_index+1]=="W" and memory =="W":
                move(memory,L,space_index)
            
            else :
                print("BLOC : [...,W,W,S,W]!")
                pass
                
        # In the rest of the algorithm, we are sure that 2 <= L.index("S") <= len(L)-3
            
        else:
            try:
                if same_color(L,space_index):

                    if can_jump("B",L,space_index) or can_jump("W",L,space_index):
                        if(L[space_index-1]=="W" and L[space_index-2]=="B"):
                            if can_jump("B",L,space_index) :
                                jump("B",L,space_index)
                                memory="B"
                            else:
                                try:
                                    move("W",L,space_index)
                                    memory="W"
                                except:
                                    print("can't move W")
                                    pass
                                    
                        elif (L[space_index+1]=="B" and L[space_index+2]=="W"):
                            if can_jump("W",L,space_index):
                                jump("W",L,space_index)
                                memory="W"
                            else:
                                try:
                                    move("B",L,space_index)
                                    memory="B"
                                except:
                                    print("can't move B")
                                    pass
                        
                    else :
                        if L[space_index-1]=="W":
                            move("W",L,space_index)
                            memory="W"
                        else :
                            move("B",L,space_index)
                            memory="B"
                else :
                    if((L[space_index-1]=="B" and memory=="B") or (L[space_index+1]=="W" and memory=="W")):
                        move(memory,L,space_index)
                    else:
                        if can_jump(memory,L,space_index):
                            jump(memory,L,space_index)
            except:
                print("Error!")
        
        print("Step {} = ".format(i),L)
        i+=1
    
def parse_arguments():
    parser = argparse.ArgumentParser(description='Sheep Problem')
    parser.add_argument('-num_Black_sheeps', '--nb_B', default=4, type=int,
                        help='number of black sheeps')
    parser.add_argument('-num_White_sheeps', '--nb_W', default=3, type=int,  
                        help='number of white sheeps')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
