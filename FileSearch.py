from pathlib import Path
from shutil import copy2
from os import utime

def whichReturn(state: str, inp: Path, printedFiles: [Path]) -> '(Path, [Path]) or Path':

    """If the user alreadly entered a second input, returns the initial input and all of the
       special files. Otherwise, returns just the initial input.
       """
    
    if state == 'second':
        return inp, printedFiles
    else:
        return inp


def fullSort(inp: Path) -> [Path]:

    """Finishes sorting the files after first calling sortUpper to sort the capitalized ones, and then
       sorting the lowercase ones and appending them to the capitalized list. Returns that list.
       """
    
    sortList = []

    UpperList = sortUpper(inp)     
 
    for x in inp.iterdir():
        if x not in UpperList:
            sortList.append(x)
    sortList.sort()

    UpperList.extend(sortList)

    return UpperList

def RD_extension_T_try(element: Path, kwargs: {str}) -> 'Path or None':

    """Attempts to read the file as text and replace the newlines with spaces."""
    
    try:
        lines = element.read_text().replace('\n',' ')
        return Tchoice(element,kwargs['userSearch'],lines,kwargs['currentState'])
    except UnicodeDecodeError:
        return None

def RD_extension(finalList: [Path], fileList: [Path], kwargs: {str}) -> [Path]:

    """Based on the second input of the user, calls a specific function and appends its output
       to a list of all of the interesting files, then returns that list.
       """
    
    for element in finalList:     
        if element.is_file() == True:
            if kwargs['action'] == 'default':
                Defaultchoice(element)
            elif kwargs['action'] == 'A':
                fileList.append(Achoice(element,kwargs['currentState']))
            elif kwargs['action'] == 'N':
                fileList.append(Nchoice(element,kwargs['userSearch'],kwargs['currentState']))
            elif kwargs['action'] == 'E':
                fileList.append(Echoice(element,kwargs['userSearch'],kwargs['currentState']))               
            elif kwargs['action'] == 'T':
                fileList.append(RD_extension_T_try(element,kwargs))
            elif kwargs['action'] == '<':
                fileList.append(lessThanChoice(element,kwargs['userSearch'],kwargs['currentState']))
            elif kwargs['action'] == '>':
                fileList.append(greaterThanChoice(element,kwargs['userSearch'],kwargs['currentState']))
                
    return fileList
  
def sortUpper(inp: Path) -> [Path]:

    """Sorts all of the capitalized files and returns them in a list so that they
       come before lowercase files when printed.
       """

    upperList = []
    
    for entry in inp.iterdir():
        the_file = entry.parts[len(entry.parts)-1]
        if str(the_file)[0].isupper() == True:
            upperList.append(entry)
        upperList.sort()

    return upperList


def TouchState(file: Path) -> None:

    """Modifies the last date of modification of the interesting file to the current one."""
    
    utime(file)

def Fstate(file: Path) -> None:

    """Tries to open the interesting file and read the first line of text.
       Prints 'NOT TEXT' if it can't open it.
       """
    
    try:
        opened_file = open(file,'r')
        print(opened_file.readline().strip())
        
    except UnicodeDecodeError:
        print('NOT TEXT')

    finally:
        opened_file.close()

def Dstate(file: Path) -> None:

    """Duplicates the interesting file in the same directory."""
    
    destination = str(file) + '.dup'
    
    copy2(str(file), destination)
    
def Defaultchoice(file: Path) -> None:

    """Prints the given file."""

    print(file)

def FDT(currentState: str, file: Path) -> None:

    """Calls a function based on what the third user input was."""
    
    if currentState == 'F':
        Fstate(file)
    elif currentState == 'D':
        Dstate(file)
    elif currentState == 'T':
        TouchState(file)

def Achoice(file: Path,currentState: str) -> Path:

    """If the state is second, print the interesting files.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if currentState == 'second':
        print(file)
        return file
    else:
        FDT(currentState, file)
    
def Nchoice(file: Path,uSearch: str,currentState:str) -> Path:

    """If the user's inputed file name matches an interesting file, print it.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if file.parts[len(file.parts)-1] == uSearch:
        if currentState == 'second':
            print(file)
            return file
        else:
            FDT(currentState, file)

def Echoice(file: Path,uSearch: str,currentState:str) -> Path:

    """If the user's inputed extension is in an interesting file, print it.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if str(file.suffix) == uSearch or (str(file.suffix) == ('.' + uSearch)):
        if currentState == 'second':
            print(file)
            return file
        else:
            FDT(currentState, file)

def Tchoice(file: Path,uSearch: str,allText: str,currentState: str) -> Path:

    """If the user's inputed text is in an interesting file, print it.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if uSearch in allText:
        if currentState == 'second':
            print(file)
            return file
        else:
            FDT(currentState, file)

def lessThanChoice(file: Path,uSearch: str,currentState: str) -> Path:

    """If the size of an interesting file is less than what the user inputed, print it.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if file.stat().st_size < int(uSearch):
        if currentState == 'second':
            print(file)
            return file
        else:
            FDT(currentState, file)

def greaterThanChoice(file: Path,uSearch: str,currentState: str) -> Path:

    """If the size of an interesting file is larger than what the user inputed, print it.
       If the state isn't second, calls FDT() to call another function.
       """
    
    if file.stat().st_size > int(uSearch):
        if currentState == 'second':
            print(file)
            return file
        else:
            FDT(currentState, file)

def Dchoice(inpD: Path, **kwargs: {str}) -> '(Path, [Path]) or Path':

    """Sorts all the files in a directory and its subdirectories through sending them to fullSort().
       Gets the interesting files from RD_extension() and calls whichReturn() to figure out what to return.
       """

    UpperList = fullSort(inpD)

    fileList = []
    
    return whichReturn(kwargs['currentState'], inpD, RD_extension(UpperList, fileList, kwargs))
    
def Rchoice(inpR: Path, fileList=[],**kwargs: {str},) -> '(Path, [Path]) or Path':
    
    """Recursively sorts all the files in a directory and its subdirectories through sending them to fullSort().
       Gets the interesting files from RD_extension() and calls whichReturn() to figure out what to return.
       """

    UpperList = fullSort(inpR)
    
    allPrintedFiles = RD_extension(UpperList, fileList, kwargs)
           
    for element in UpperList:
        if element.is_dir() == True:
            if kwargs['action'] != 'default':
                Rchoice(element, fileList=allPrintedFiles, action=kwargs['action'], userSearch=kwargs['userSearch'], currentState=kwargs['currentState'])
            else: 
                Rchoice(element, fileList=allPrintedFiles, action='default',currentState='first')

    return whichReturn(kwargs['currentState'], inpR, allPrintedFiles)
    
    
def chooseSecondAction(firstChoice: str,initialInput: Path) -> None:
    """Asks user for second input, makes sure that it's valid, and then sends it to SecondActionPush()."""
    
    kwargList = ['default','A','N','E','T','<','>']
    action2 = input().split(' ', 1)
    action2.append(' ')
    
    if action2[0] in kwargList and (action2[0] == 'default' or action2[0] == 'A') or ((action2[0] == 'N' or action2[0] == 'E' or action2[0] == 'T' or action2[0] == '<' or action2[0] == '>')
    and (' ' not in action2[1] and action2[1] != None and action2[1] != '')): 
        if (action2[0] == '<' or action2[0] == '>'):
            try:
                int(action2[1])
            except:
                print('ERROR')
                chooseSecondAction(firstChoice, initialInput)
            else:
                SecondActionPush(firstChoice, initialInput, action2[0], action2[1]) 
        else:    
            SecondActionPush(firstChoice, initialInput, action2[0], action2[1])
        
    else: 
        print('ERROR')
        chooseSecondAction(firstChoice, initialInput)

def chooseThirdAction(firstChoice: str,initialInput: (Path, [Path]),action2: str,userSearch: str) -> None:
    """Checks to see if there are entries that an action can be taken on. If there are, send info to ThirdActionPush()."""
    
    noneCount = 0
    for i in initialInput[1]:
        if i == None:
            noneCount += 1

    if noneCount < len(initialInput[1]):
        actionList = ['F','D','T']
        action3 = input()
        if action3 not in actionList:
            print('ERROR')
            chooseThirdAction(firstChoice, initialInput, action2, userSearch)
        else:
            ThirdActionPush(firstChoice,initialInput[0],action2,action3,userSearch)

def ThirdActionPush(firstChoice: str,initialInput: Path,action2: str,action3: str,userSrch: str) -> None:
    """Takes info from chooseThirdAction() and sends it to Dchoice or Rchoice."""
    
    if firstChoice == 'D':
        Dchoice(initialInput, action=action2, userSearch=userSrch, currentState=action3)
    elif firstChoice == 'R':
        Rchoice(initialInput, action=action2, userSearch=userSrch, currentState=action3)


def SecondActionPush(frstChoice: str, initInp: Path, actn: str, userSrch: str) -> None:
    """Takes info from chooseSecondAction(), sends it to Dchoice or Rchoice, calls chooseThirdAction() from it."""
    
    if frstChoice == 'D':
        chooseThirdAction('D',Dchoice(initInp, action=actn, userSearch=userSrch, currentState='second'),actn,userSrch)
    elif frstChoice == 'R':
        chooseThirdAction('R',Rchoice(initInp, action=actn, userSearch=userSrch, currentState='second'),actn,userSrch)
    
def chooseFirstAction() -> None:
    """Allows user to enter D or R followed by a path, and checks that they entered an existing directory."""
    
    while True:
        initInp = input()
        inp = initInp.split(' ',1)
        inp.append('')
        try:
            p = Path(inp[1])
            if p.is_dir() == True and p.exists() == True and inp[1] != '':
                if inp[0] == 'D':
                    chooseSecondAction('D', Dchoice(p, action='default',currentState='first'))
                    break
                elif inp[0] == 'R':
                    chooseSecondAction('R', Rchoice(p, action='default',currentState='first'))
                    break
                else:
                    print("ERROR")
            else:
                print("ERROR")
        except:
            print("ERROR")
           
if __name__ == '__main__':
    chooseFirstAction()



