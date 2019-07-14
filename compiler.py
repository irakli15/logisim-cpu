import sys
import struct

class Compiler:
  arithmetic = {
    "A" : 0, 
    "B" : 1, 
    "+" : 2,
    "-" : 3,
    "*" : 4,
    "&" : 5,
    "|" : 6,
    "!A": 7
  }
  memoryLocation = {
  "A" : 0,
  "D" : 1,
  "M" : 2,
  "num":3
  }
  cmpValues = {
    "BEQ" : 2,
    "BGT" : 1,
    "BLT" : 4
  }

  alu = 0
  inp1 = 1  
  inp2 = 2    
  a = 3       
  aluInp1 = 4 
  aluInp2 = 5 
  aluOut = 6 
  jumpInp = 7
  condJump = 8

  def __init__(self, fileName):
    inFile = open(fileName, "r")
    self.outFile = open("binary", "w")
    self.outFile.write("v2.0 raw\n")
    self.data = {
      self.alu       : 0,  #4
      self.inp1      : 0,  #8
      self.inp2      : 0,  #8
      self.a         : 0,  #1
      self.aluInp1   : 0,  #2
      self.aluInp2   : 0,  #2
      self.aluOut    : 0,  #2
      self.jumpInp   : 0,  #1
      self.condJump  : 0   #3
    }
    self.lineCount = 0
    self.labels = {}

    for line in inFile:
      self.clearData()
      if len(line) == 1:
        continue
      if self.compile(line.upper().split()) == 1:
        continue
      # print(line.split())
      self.pack()
      self.lineCount += 1

  def pack(self):
    result = ""
    result += self.numToStr(self.data[self.alu]).zfill(4)
    result += self.numToStr(self.data[self.inp1]).zfill(8)
    result += self.numToStr(self.data[self.inp2]).zfill(8)
    result += self.numToStr(self.data[self.a]).zfill(1)
    result += self.numToStr(self.data[self.aluInp1]).zfill(2)
    result += self.numToStr(self.data[self.aluInp2]).zfill(2)
    result += self.numToStr(self.data[self.aluOut]).zfill(2)
    result += self.numToStr(self.data[self.jumpInp]).zfill(2)
    result += self.numToStr(self.data[self.condJump]).zfill(3)
    print(result)
    print()
    self.outFile.write(hex(int(result, 2))[2:] + "\n")
  
  def clearData(self):
    for key in self.data:
      self.data[key] = 0



  def numToStr(self, num):
    # print (bin(num)[2:])

    return bin(num)[2:]

  def handleMemLocation(self, line, i, where):
    print(line[i]+"****")
    if line[i] in self.memoryLocation :
      self.data[where] = self.memoryLocation[line[i]]
    elif str.isdecimal(line[i]):
      self.data[where] = self.memoryLocation["num"]

  def compile(self, line):
    print(line)
    if(line[0] == '('):
      self.labels[line[1]] = self.lineCount
      return 1
  
    if(line[0] == "@"):
      if(line[1].isdecimal()):
        self.data[self.inp1]=int(line[1])
        self.data[self.a] = 1
        return
      else:
        self.data[self.inp1]=self.labels[line[1]]
        self.data[self.a] = 1
        print("addr "+str(self.labels[line[1]]) )
        return


    if(line[0] == "JMP"):
      self.handleMemLocation(line, 1, self.jumpInp)

      # self.handleMemLocation(line, 0, self.condJump)

      if(line[1].isdecimal()):
        self.data[self.inp2]=int(line[1])
      self.data[self.aluInp1] = 0
      self.data[self.aluInp2] = 0
      self.data[self.condJump] = 2
      return
    
    if(line[0] in self.cmpValues):
      # can't do both
      # assert(line[1].isdecimal() != line[2].isdecimal())
      self.handleMemLocation(line, 1, self.aluInp1)
      self.handleMemLocation(line, 2, self.aluInp2)

      if(line[1].isdecimal()):
        print(line[1]+"----")
        self.data[self.inp1]=int(line[1])

      if(line[2].isdecimal()):
        self.data[self.inp1]=int(line[2])

      
      self.data[self.condJump] = self.cmpValues[line[0]]
      self.data[self.jumpInp] = 0

      # if(line[3].isdecimal()):
      #   self.data[self.jumpInp] = 3
      #   self.data[self.inp2] = int(line[3])
      return







    # print(line[0])
    if line[0] in self.memoryLocation :
      self.data[self.aluOut] = self.memoryLocation[line[0]]
      print(self.data[self.aluOut])
    
    assert(line[1] == "=")

    self.handleMemLocation(line, 2, self.aluInp1)
    if(line[2].isdecimal()):
      self.data[self.inp1] = int(line[2])

    if(len(line) == 3):
      return

    print(len(line))

    self.data[self.alu] = self.arithmetic[line[3]]

    self.handleMemLocation(line, 4, self.aluInp2)

    


    

      




if __name__ == "__main__":
    compiler = Compiler(sys.argv[1])
