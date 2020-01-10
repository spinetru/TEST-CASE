#!/usr/bin/env python
# -*- coding: utf-8 -*-

def check_bit_correct(segm, checkbit, maskcheck):
	y= segm & checkbit
	x= segm & maskcheck
#	print('------------------y,x=',bin(y), bin(x))
	i=0
	while (x>0):
		if (x%2 >0):
			 i=i+1
		x=x>>1
#	print('--------------segm:',bin(segm), '  y=',bin(y), '  x=',bin(x), '  i=',i)
	if (0==i%2) :
		return 1
	else:
		return 0


def check(segm):
        parity_error=0
        corr_bit=1
	#1bit
        if check_bit_correct(segm,0b100000000000000, 0b101010101010101):
                parity_error+=0
        else:
                parity_error+=1
	#2bit
        if check_bit_correct(segm,0b010000000000000, 0b011001100110011):
                parity_error+=0
        else:
                parity_error+=2
	#4bit
        if check_bit_correct(segm,0b000100000000000, 0b000111100001111):
                parity_error+=0
        else:
                parity_error+=4
	#8bit
        if check_bit_correct(segm,0b000000010000000, 0b000000011111111):
                parity_error+=0
        else:
                parity_error+=8

        if parity_error==0:
                return segm
        else:
#		print ('-----ERRORvvvv----------')
#		print ('corr1: ', bin(corr_bit), 'corr_shift: ', bin(corr_bit<<(15-parity_error)))
                corrb = segm^(corr_bit<<(15-parity_error))
#		print ('ERROR ',parity_error, bin(segm), 'corr: ', bin(corrb))
                return  corrb
#end def check()


file=open('testmessage.bin','rb')
file.seek(4)
code=0
i=0
tbyte=0
while 1:
	while(i<15):
		b1code=file.read(1)
		i=i+8
		if not b1code:
			break
		code=(code<<8)|ord(b1code) #получаем в code кусок max размером до 16 байт
	if not b1code:
		break
	#схема битов: корректирующие отмечены p: "pp_p___p_______"
	if tbyte==0:
		segm15= code>>(i-15)   #Нужны в segm15 15 бит. Удаляем смещением лишний байт 'pp1p234p56789ABx' -> 'pp1p234p56789AB'
	else:
		segm15= code>>(i-15)
		segm15= segm15|tbyte   #добавляем биты из прошлого набора '000p123p56789AB'|'pp1000000000000'
	tbyte= (code& ( 2**(i-15)-1 ) )<< (15-(i-15)) # сохраняем в tbyte набор "лишних" бит 'xxxxxxxxxxxxpp1'&'000000000000111' << -> 'pp1000000000000'

	s=check(segm15)
	print (format(s, 'b').zfill(15))
	code=0
	i=i-15
	#print(code)


file.close()



#filew=open('l4checkcode','wb')

