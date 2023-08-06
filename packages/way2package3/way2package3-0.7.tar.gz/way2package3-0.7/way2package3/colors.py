class colors:
    pickColor = {
        "default":{
            "reset":'\033[0m',
            "bold":'\033[01m',
            "disable":'\033[02m',
            "underline":'\033[04m',
            "reverse":'\033[07m',
            "strikethrough":'\033[09m',
            "invisible":'\033[08m'
        },
        "foreground":{
            "black":'\033[30m',
            "red":'\033[31m',
            "green":'\033[32m',
            "orange":'\033[33m',
            "blue":'\033[34m',
            "purple":'\033[35m',
            "cyan":'\033[36m',
            "lightgrey":'\033[37m',
            "darkgrey":'\033[90m',
            "lightred":'\033[91m',
            "lightgreen":'\033[92m',
            "yellow":'\033[93m',
            "lightblue":'\033[94m',
            "pink":'\033[95m',
            "lightcyan":'\033[96m',
        }, 
        "background":{
            "black":'\033[40m',
            "red":'\033[41m',
            "green":'\033[42m',
            "orange":'\033[43m',
            "blue":'\033[44m',
            "purple":'\033[45m',
            "cyan":'\033[46m',
            "lightgrey":'\033[ 47m'
        }
    }


strings = []
msg = '''
\033[32m
Importing: \033[0m
   import way2package3 
\033[32m
Create instance of 'Myclass' in way2package3 module \033[0m
   name = "Mohammed" #name should be required
   colorObj = way2package3.Myclass(name) 
\033[32m
Calling methods \033[0m
   requirements = {
    "foreground":"red",
    "background":"green",
    "extra":"underline" 
   }
   colorObj.sayHai(requirements)
              (or)
   colorObj.sayBye(requirements)
   
'''
print("\033[37m\033[04m\033[01mGuide:\033[0m",msg)
# message = "\n\033[35m#extraList:\n \033[36m\033[36m{}\n\033[35m#foregroundList:\n \033[36m{}\n\033[35m#backgroundList:\n \033[36m{}\n\033[0m".format(list(colors.pickColor["default"].keys()),list(colors.pickColor["foreground"].keys()),list(colors.pickColor["background"].keys()))
# print("\n\033[04m\033[32m Options:\n\033[0m",message)