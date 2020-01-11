#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

def check_bit_correct(segm, checkbit, maskcheck):
	y= segm & checkbit
	x= segm & maskcheck
	i=0
	while (x>0):
		if (x%2 >0):
			 i=i+1
		x=x>>1
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
                corrb = segm^(corr_bit<<(15-parity_error))
                return  corrb
#end def check()




def mainprog(f1,f2):
 file=open(f1,'rb')
 file.seek(4)
 code=0
 i=0
 tbyte=0
 fw=open(f2,'wb')
 k=3
 tmp=0
 while 1:
  while(i<15):  #i необходимо для проверки сколько байт читать из файла
   b1code=file.read(1)
   i=i+8
   if not b1code:
    break
   code=(code<<8)|ord(b1code) #получаем в code кусок max размером до 16 байт
  if not b1code:
   break
	#схема битов: x- "лишний" для кода. Корректирующие отмечены p: "pp_p___p_______x"
  if tbyte==0:
   segm15= code>>(i-15)   #Нужны в segm15 15 бит. Удаляем смещением лишний бит 'pp1p234p56789ABx' -> 'pp1p234p56789AB'
  else:
   segm15= code>>(i-15)
   segm15= segm15|tbyte   #добавляем биты из прошлого набора '000p123p56789AB'|'pp1000000000000'
  tbyte= (code& ( 2**(i-15)-1 ) )<< (15-(i-15)) # сохраняем в tbyte набор "лишних" бит 'xxxxxxxxxxxxpp1'&'000000000000111' << -> 'pp1000000000000'

  s=check(segm15)
	#print (format(s, 'b').zfill(15))  
  s11=s&0b1111111             #Удаление контрольных битов, далее они не нужны 'pp1p234p56789AB' -> '123456789AB'
  s11=((s>>1)&0b1110000000)|s11
  s11=((s>>2)&0b10000000000)|s11
  s=s11

#Ниже код склеивает/делит из считанного сегмента на отрезки по 8/16бит
  if k==3:
   b2w= s>>k
   tmp = s&0b111
  if k==6:
   b2w =(tmp<<5)|(s>>k) 
   tmp = s&0b111111
  if k==1:
   b2w= (tmp<<10)|(s>>k)
   tmp = s&0b1
  if k==4:
   b2w=(tmp<<7)|(s>>k)
   tmp =s&0b1111
  if k==7:
   b2w= (tmp<<4)|(s>>k)
   tmp= s&0b1111111
  if k==2:
   b2w=(tmp<<9)|(s>>k)
   tmp=s&0b11
  if k==5:
   b2w = (tmp<<6)|(s>>k)
   tmp=s&0b11111
  if k==0:
   b2w=(tmp<<11)|s
   tmp=0

  if k<3:            #обработка и запись в файл 8/16 бит. k вычисленно по таблице
   fw.write(bytearray(([b2w>>8])))
   fw.write(bytearray(([b2w&0b11111111])))
  else:
   fw.write(bytearray(([b2w])))

  k=(k+3)&0b111 #счетчик остатка от 11бит декодированного сегмета после записи в файл 8/16 бит
  code=0
  i=i-15 

 fw.close()
 file.close()



#main prog
if (len(sys.argv)<3):
	print ('Use: ', sys.argv[0], 'file.encode file.to.decode' )
else:
	mainprog(sys.argv[1], sys.argv[2])
