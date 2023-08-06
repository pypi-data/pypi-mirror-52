from omegamath01 import OmegaMath01 as h
class encode:
    def caesar(text,codeword):
      var = str(codeword)
      a=0
      print()
      var1 = "abcdefghijklmnopqrstuvwxyz"
      while int(a) < len(var):
        var1 = var1.replace( var[a], "")
        a += 1

      intab = "abcdefghijklmnopqrstuvwxyz"
      outtab = str(var + var1) 




      a=h.Func.MakeTrans(intab,outtab)

      a.change(str(text))
    def railroad(text):
       string1 = str(text)
       string = string1.replace(' ','')
       var=len(string)

       if int(var)<28:
          for i in [1,2,3,4,5,5,6,7,8,9,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,0]:
             string = string + str(i)
             if len(string)>=28:
                break
           
       if len(string) > 27:
         a=string[0:4]
         b=string[4:8]
         c=string[8:12]
         d=string[12:16]
         e=string[16:20]
         f=string[20:24]
         g=string[24:28]
         a1=a[0:1] + b[0:1] + c[0:1] + d[0:1] + e[0:1] + f[0:1] + g[0:1]
         a2=a[1:2] + b[1:2] + c[1:2] + d[1:2] + e[1:2] + f[1:2] + g[1:2]
         a3=a[2:3] + b[2:3] + c[2:3] + d[2:3] + e[2:3] + f[2:3] + g[2:3]
         a4=a[3:4] + b[3:4] + c[3:4] + d[3:4] + e[3:4] + f[3:4] + g[3:4]
         mes= a1 + ' ' +a2 + " " +a3 +' '+a4

       return(mes)
    def abc_square(text):
        a=["a","b","c","d","e"]
        b=["f","g","h","i","k"]
        c=["l","m","n","o","p"]
        d=["q","r","s","t","u"]
        e=["v","w","x","y","z"]
        text1=[str(text[i:i+1]) for i in range(len(text))]
        pos1=[]
        for i in text1:
            if i =="j":
                i="i"
            if i in a:
                pos1.append(str(1)+str(int((a.index(i))+1)))
            if i in b:
                pos1.append(str(2)+str(int((b.index(i))+1)))
            if i in c:
                pos1.append(str(3)+str(int((c.index(i))+1)))
            if i in d:
                pos1.append(str(4)+str(int((d.index(i))+1)))
            if i in e:
                pos1.append(str(5)+str(int((e.index(i))+1)))
        pos=""
        for i in pos1:
            pos=pos+" "+str(i)
        print(pos)
class decode:
    def caesar_dec(text,codeword):
      #Hub is the encoded message you recieved.
      hub = str(text)


      #var2 is the codeword you are using to decode it.
      var2 = str(codeword)

      b=0
      var3 = "abcdefghijklmnopqrstuvwxyz"
      alpha= "abcdefghijklmnopqrstuvwxyz"
      while int(b) < len(var2):
        var3 = var3.replace( var2[b], "")
        b += 1

      outtab2 = str(var2 +var3)
      metatab = h.Func.MakeTrans(outtab2, alpha)

      metatab.change(hub)
    def railroad_dec(text):
        string1 = str(text)
        string = string1.replace(' ', '')
        var = len(string)
        
        a1 = string[0:7]
        a2 = string[7:14]
        a3 = string[14:21]
        a4 = string[21:28]
        a=a1[0:1] + a2[0:1] +a3[0:1] + a4[0:1]
        b=a1[1:2] + a2[1:2] +a3[1:2] + a4[1:2]
        c=a1[2:3] + a2[2:3] +a3[2:3] + a4[2:3]
        d=a1[3:4] + a2[3:4] +a3[3:4] + a4[3:4]
        e=a1[4:5] + a2[4:5] +a3[4:5] + a4[4:5]
        f=a1[5:6] + a2[5:6] +a3[5:6] + a4[5:6]
        g=a1[6:7] + a2[6:7] +a3[6:7] + a4[6:7]
        mes=a+b+c+d+e+f+g
        mes = mes.replace("1", '')
        mes = mes.replace("2", '')
        mes = mes.replace("3", '')
        mes = mes.replace("4", '')
        mes = mes.replace("5", '')
        mes = mes.replace("6", '')
        mes = mes.replace("7", '')
        mes = mes.replace("8", '')
        mes = mes.replace("9", '')
        mes = mes.replace("0", '')
        return(mes)
    def abc_square_dec(text):
        text=str(text).replace(" ","")
        num=[]
        for i in range(len(text)):
            if i%2==0:
                       num.append(text[i:i+2])
        abc="abcdefghiklmonpqrstuvwxyz"
        ret="" 
        for i in num:
            if i[0:1]=="1":
                if i[1:2]=="1":
                    ret=ret+"a"
                if i[1:2]=="2":
                    ret=ret+"b"
                if i[1:2]=="3":
                    ret=ret+"c"
                if i[1:2]=="4":
                    ret=ret+"d"
                if i[1:2]=="5":
                    ret=ret+"e"
            if i[0:1]=="2":
                if i[1:2]=="1":
                    ret=ret+"f"
                if i[1:2]=="2":
                    ret=ret+"g"
                if i[1:2]=="3":
                    ret=ret+"h"
                if i[1:2]=="4":
                    ret=ret+"i"
                if i[1:2]=="5":
                    ret=ret+"k"
            if i[0:1]=="3":
                if i[1:2]=="1":
                    ret=ret+"l"
                if i[1:2]=="2":
                    ret=ret+"m"
                if i[1:2]=="3":
                    ret=ret+"n"
                if i[1:2]=="4":
                    ret=ret+"o"
                if i[1:2]=="5":
                    ret=ret+"p"
            if i[0:1]=="4":
                if i[1:2]=="1":
                    ret=ret+"q"
                if i[1:2]=="2":
                    ret=ret+"r"
                if i[1:2]=="3":
                    ret=ret+"s"
                if i[1:2]=="4":
                    ret=ret+"t"
                if i[1:2]=="5":
                    ret=ret+"u"
            if i[0:1]=="5":
                if i[1:2]=="1":
                    ret=ret+"v"
                if i[1:2]=="2":
                    ret=ret+"w"
                if i[1:2]=="3":
                    ret=ret+"x"
                if i[1:2]=="4":
                    ret=ret+"y"
                if i[1:2]=="5":
                    ret=ret+"z"
        print(ret)


