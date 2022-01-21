# F4 DataCrawler

Serve para:
  - Busca recursiva por arquivos de uma determinada extensão. (ex: -simple txt pdf xlsx)
  - Busca recursiva por arquivos de uma determinada extensão, lê esses arquivos e procurar o que você quiser através do RegEx que você passar, como cpf, rg, ip,etc... (ex: main.py -r '\d{3}\.\d{3}\.\d{3}-\d{2}' -v -xlsx).     

Você pode:
  - Salvar a saída em um arquivo da sua escolha(-s saida.txt)
  - Escolher se quer ver os valores(-v) referentes ao RegEx que você passar (já vem com as opções: -cpf, -rg, -ip, -visa, -mc(master card)), a linha(-l) em que o valor se encontra em cada arquivo ou caso o valor esteja em meio a um texto mair dentro de excel (ex: joao da silva: cfp 999.999.999-99), você pode usar -full para ver o texto completo em que o valor se encontra.
  - Escolher o tipo de arquivo que você quer buscar: -xlsx (.xlsx/.xls) ou -txt (.txt)
  - Escolher que quer ver ou não os erros ( caso ocorra algum erro ao abrir ou ler algum arquivo) usando o -e ou --NoError caso não queira ver os erros.
  - Escolher um PATH de início para a busca recursiva(-p C:\Users\F4\Desktop)
  - Escolher um arquivo específico(-file) e buscar algo dentro dele através de um RegEx (ex: main.py -r cpf -file File.xlsx -v -xlsx)

~ F4 | https://beacons.ai/f4_zzz
