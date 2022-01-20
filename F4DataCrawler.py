import argparse, re, glob
import pandas as pd
from prettytable import PrettyTable

#####################################  Arg Parse #################################
parser = argparse.ArgumentParser()
parser.add_argument("-p","--StartPath", nargs=1, help="Start Path", required=False, default='./', dest="path")
parser.add_argument("-r","--regex",nargs=1, help="Tipo: cpf, rg ou ip",default=False, required=False, dest="regex")
parser.add_argument("-file", nargs=1, help="Nome do arquivo + extenção", required=False, default=False, dest="file")
parser.add_argument("-s","--save",nargs=1, help="Nome do arquivo onde deseja salvar o output + extenção",default=False, required=False, dest="txtsave")
parser.add_argument("-v","--value",help="Mostrar apenas os values",default=False, required=False, action="store_true", dest="value")
parser.add_argument("-l","--line",help="Mostrar as linhas em que os values aparecem",default=False, required=False, action="store_true", dest="lines")
parser.add_argument("--full",help="Dumpar todas as linhas em que os values aparecem",default=False, required=False, action="store_true", dest="full")
parser.add_argument("-simple",nargs='+' ,help="Busca por extenções e mostra o PATH",default=False, required=False, type=list, dest="SimpleSearch")
parser.add_argument("-xlsx","--excel",help="Busca por aquivos .xlsx e xls",default=False, required=False, action="store_true", dest="xlsxFileOpt")
parser.add_argument("-txt",help="Busca por aquivos .txt",default=False, required=False, action="store_true", dest="txtFileOpt")
parser.add_argument("-readme",help="Use this for + info",default=False, required=False, action="store_true", dest="readmeMenu")
parser.add_argument("-e", "--NoError",help="Don't show errors",default=False, required=False, action="store_true", dest="noerror")
mainarg= parser.parse_args()

UsrFile = mainarg.file
path = mainarg.path[0]
valuesOpt=mainarg.value
linesOpt=mainarg.lines
fullOpt=mainarg.full
txtsave = mainarg.txtsave
xlsxFileOpt = mainarg.xlsxFileOpt
txtFileOpt = mainarg.txtFileOpt
readmeMenu = mainarg.readmeMenu
SimpleSearch = mainarg.SimpleSearch
tipo = mainarg.regex
noerror = mainarg.noerror

def txtlog(text):
    with open(str(txtsave[0]), "a") as txt:
        txt.write(f'{text}\n')

###########################  Readme Pretty Table  ##########################################
if readmeMenu != False:
    readmeTB = PrettyTable()
    readmeTB.title = "F4 Data Crawler | Help"
    readmeTB.field_names = ['arg', 'objective', 'exemple']
    readmeTB.add_row(['-p --StartPath', 'Set a start path', rf'main.py -r cpf -p C:\Users\F4\Desktop -v -xlsx'])
    readmeTB.add_row(['-r --regex', 'Set a RegEx (cpf, rg, ip, visa, mc or your own RegEx)', r"main.py -r cpf -v OR main.py -r '\d{3}\.\d{3}\.\d{3}-\d{2}' -v -xlsx"])
    readmeTB.add_row(['-file', 'Set a especific file', 'main.py -r cpf -file File.xlsx -v -xlsx'])
    readmeTB.add_row(['-s --save', 'Set a file to save the output', 'main.py -r cpf -s cpfdump.txt -v -xlsx'])
    readmeTB.add_row(['-v --value', 'Show only the values', 'main.py -r cpf -v -xlsx'])
    readmeTB.add_row(['-l --line', 'Show the line where the value is', 'main.py -r cpf -l -xlsx'])
    readmeTB.add_row(['-simple', 'Search for extensions and show the PATH', 'main.py -simple xlsx txt pdf'])
    readmeTB.add_row(['--full', 'Show the full text where the regex was found (xls/xlsx only)', 'main.py -r cpf -full -xlsx'])
    readmeTB.add_row(['-xlsx --excel', 'Search for xls/xlsx files', 'main.py -r cpf -v -xlsx'])
    readmeTB.add_row(['-txt', 'Search for txt files', 'main.py -r cpf -v -txt'])
    readmeTB.add_row(['-e --NoError', "Don't show errors", 'main.py -r cpf -v -txt -e'])
    print(readmeTB)
    exit()

##############################   -simple    #############################################
if SimpleSearch != False:

    simpleTB = PrettyTable()
    simpleTB.title = "F4 Data Crawler"
    simpleTB.field_names = ['ext', 'PATH']

    for SubList in SimpleSearch:
        NewSubList = ''.join(SubList)
 
        for SimpleFile in glob.glob(rf"{path}\**",recursive=True):
            if SimpleFile.endswith(f"{NewSubList}"):
                #print(NewSubList, '   ', SimpleFile)

                simpleTB.add_row([NewSubList, SimpleFile])
    
    print(simpleTB)
    if mainarg.txtsave != False: txtlog(simpleTB) 
    #exit()

############################ error ####################################
if xlsxFileOpt == False and txtFileOpt == False:
    if SimpleSearch == False:
        exit(code='You have to choose a file type (-xlsx, -txt or both)... use -readme for + info :)')

if tipo == False:
    if SimpleSearch == False:
        exit(code='You need to choose a RegEx... use -readme for + info :)')
else: tipo = mainarg.regex[0]

########################### Options pretty table ##########################
ftab=PrettyTable()
ftab.title = "F4 Data Crawler | Options"
ftab.field_names = ['Options', 'Answers']
ftab.add_row(['Given File:', UsrFile])
ftab.add_row(['Given Path:', path])
ftab.add_row(["Don't show errors", noerror])
ftab.add_row(['Save Output:', txtsave])
ftab.add_row(['RegEx Type:', tipo])
ftab.add_row(['Show Values:', valuesOpt])
ftab.add_row(['Show Lines:', linesOpt])
ftab.add_row(['Show Full:', fullOpt])
ftab.add_row(['FileType xlsx|xls:', xlsxFileOpt])
ftab.add_row(['FileType .txt:', txtFileOpt])
if SimpleSearch == False:
    print(ftab)

##########################################################################################
if mainarg.txtsave != False:
    txtlog(ftab)  

findCpf=r"\d{3}\.\d{3}\.\d{3}-\d{2}"
findRg=r"(^(\d{2}\x2E\d{3}\x2E\d{3}[-]\d{1})$|^(\d{2}\x2E\d{3}\x2E\d{3})$)"
findIp=r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}[^0-9]"
findVisa=r"^4[0-9]{12}(?:[0-9]{3})?$"
findMasterCard=r"^5[1-5][0-9]{14}$"

if tipo == 'cpf': regex=findCpf
elif tipo == 'rg': regex=findRg
elif tipo == 'ip': regex=findIp
elif tipo == 'visa': regex=findVisa
elif tipo == 'mc': regex=findMasterCard
else: regex = tipo

for excel in glob.glob(rf"{path}\**",recursive=True):
    mainTB=PrettyTable()
    mainTB.title = "F4 Data Crawler"
    mainTB.field_names = [excel]

    errorTB=PrettyTable()
    errorTB.title = "F4 Data Crawler | Error"
    errorTB.field_names = ['PATH', 'Error']

    if xlsxFileOpt != False:

        if(excel.endswith("xls") or excel.endswith("xlsx")):

            if mainarg.value == False and mainarg.lines == False and mainarg.full == False:
                exit(code='\nEscolha uma opção: -v , -l ou -f  |  -readme para mais informações :)\n')

            toRead = excel[2:]
            if UsrFile != False:
                toRead = UsrFile[0]

            try:
                tabela = pd.read_excel(str(toRead))      

                values=[];lines=[];frases=[];taok=[]

                for coluna in tabela.columns:

                    line = 2
                    for i in tabela[str(coluna)]:
                        match = regex
                        value = re.findall(match, str(i))
                        if value != []:
                            taok.append(coluna)
                            values.append(value)
                            lines.append(line)
                        line+=1

                    if coluna in taok:
                        for i in lines:          
                            frase = str(tabela.loc[i-2][str(coluna)])
                            frases.append(frase.strip())

                val = ''
                if mainarg.value == True:
                    for value in values:
                        for val in value:
                            mainTB.add_row([val])
                    if val != '': 
                        print(mainTB)
                        if mainarg.txtsave != False: txtlog(mainTB)
                        
                line = ''
                if mainarg.lines == True:
                    for line in lines:
                        mainTB.add_row([line])
                    if line != '': 
                        print(mainTB)
                        if mainarg.txtsave != False: txtlog(mainTB)
                            
                frase = ''
                if mainarg.full == True:
                    for frase in frases:
                        mainTB.add_row([frase])
                    if frase != '': 
                        print(mainTB)      
                        if mainarg.txtsave != False: txtlog(mainTB)              
                if UsrFile != False: exit()
            except Exception as ex:
                if noerror == False:
                    print(f'\nError: {ex}\nPath: {toRead}\n')
                

    if txtFileOpt != False:
        if excel.endswith("txt"):
            txtvalues=[];txtlines=[]

            FilePorra = excel
            if UsrFile != False:
                FilePorra = UsrFile[0]             

            txtline = 1
            try:
                with open(FilePorra, 'r') as txtfile:
                    for objc in txtfile.readlines():
                        revalue = re.findall(regex, objc)
                        if revalue != []:
                            txtvalues.append(revalue[0])
                            txtlines.append(txtline)
                        txtline+=1
            except Exception as ex:
                if noerror == False:
                    print(f'\nError: {ex}\nPath: {FilePorra}\n')
                

            if mainarg.value == True:
                if revalue != []:
                    for revalue in txtvalues:
                        mainTB.add_row([revalue])
                    print(mainTB)
                    if mainarg.txtsave != False: txtlog(mainTB)
                                     
            if mainarg.lines == True:
                if revalue != []:
                    for txtline in txtlines:
                        print(txtline)
                        mainTB.add_row([txtline])
                    print(mainTB)
                    if mainarg.txtsave != False: txtlog(mainTB)

            if UsrFile != False: exit()  

# F4 ~ https://beacons.ai/f4_zzz