from way2package3.colors import colors
class Myclass:
    def __init__(self,username):
        if(not isinstance(username,str)): return "Sorry!..username must be string."
        self.name = username
    def sayHai(self,color):
        print(colors.fg.blue, colors.bold,colors.underline,"woww asdf Amartya",colors.reset)
        print("\033[96m Hai '{}'.\033[00m".format(self.name))
        return "Hai '{}'.".format(self.name)
    def sayBye(self):
        print("Bye..miss you '{}'".format(self.name))
        return "Bye..miss you '{}'".format(self.name)

