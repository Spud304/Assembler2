#define test_var 0x7DE

LVX 0x0                         ;Resetting vars
STX 0x7DD label:                ;counter1 1
STX test_var                       ;counter1 2
STX 0x7DF                       ;counter1 3   use this for timing 
STX 0x7E0                       ;counter2 1   note timing 
STX 0x7E1                       ;counter2 2   note timing 
STX 0x7E2                       ;timing comp value
LVY 0xF
STY 0x7E3                       ;tone comp low
STY 0x7E4                       ;tone comp high
STX 0x7E5    