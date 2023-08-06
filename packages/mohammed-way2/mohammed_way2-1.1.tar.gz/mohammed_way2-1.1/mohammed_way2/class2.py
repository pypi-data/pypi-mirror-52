from way2package3.colors import colors
msg = '''
\033[32m
Importing: \033[0m
   import mohammed_way2 
\033[32m
Create instance of 'Myclass' in mohammed_way2 module \033[0m
   name = "Mohammed" #name should be required
   colorObj = mohammed_way2.Myclass(name) 
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

   #To watch options available for requirements
   #   colortObj.optionsAvailable()
'''
class Myclass:
    def __init__(self,username):
        if(not isinstance(username,str)):
            print("Sorry!..username must be string.")
            return "Sorry!..username must be string."
        self.name = username
    def sayHai(self,obj=None):
        try:
            strings = []
            if(not isinstance(obj,dict)):
                print("Sorry!.. must pass an object.")
                return "Sorry!.. must pass an object." 
            for key in obj:
                if(key == 'foreground'):
                    strings.append(colors.pickColor["foreground"][obj[key]])
                elif(key == 'extra'):
                    strings.append(colors.pickColor["default"][obj[key]])
                elif(key == 'background'):
                    strings.append(colors.pickColor["background"][obj[key]])
                else:
                    return "Sorry!.. {} option not found.".format(key)
            if(len(strings) == 0): strings.append(colors.pickColor["foreground"]["blue"])
            message = " ".join(strings)
            print(message,"Hai '{}'.".format(self.name),colors.pickColor["default"]["reset"])
            return "Hai '{}'.".format(self.name)
        except Exception as e:
            print(colors.pickColor["foreground"]["red"],"Oops..We are facing following issue:\n",str(e),colors.pickColor["default"]["reset"])
            return
    def sayBye(self,obj=None):
        try:
            strings = []
            if(not isinstance(obj,dict)):
                print("Sorry!.. must pass an object.")
                return "Sorry!.. must pass an object."            
            for key in obj:
                if(key == 'foreground'):
                    strings.append(colors.pickColor["foreground"][obj[key]])
                elif(key == 'extra'):
                    strings.append(colors.pickColor["default"][obj[key]])
                elif(key == 'background'):
                    strings.append(colors.pickColor["background"][obj[key]])
                else:
                    return "Sorry!.. {} option not found.".format(key)
            if(len(strings) == 0): strings.append(colors.pickColor["foreground"]["blue"])
            message = " ".join(strings)
            print(message,"Bye..miss you '{}'".format(self.name),colors.pickColor["default"]["reset"])
            return "Bye..miss you '{}'".format(self.name)
        except Exception as e:
            print(colors.pickColor["foreground"]["red"],"Oops..We are facing following issue:\n",str(e),colors.pickColor["default"]["reset"])
            return
        
    def help(self):
        global msg
        print(msg)
        return
    
    def optionsAvailable():
        message = "\n\033[35m#extraList:\n \033[36m\033[36m{}\n\033[35m#foregroundList:\n \033[36m{}\n\033[35m#backgroundList:\n \033[36m{}\n\033[0m".format(list(colors.pickColor["default"].keys()),list(colors.pickColor["foreground"].keys()),list(colors.pickColor["background"].keys()))
        print("\n\033[04m\033[32m\033[01m Options:\n\033[0m",message)
        return