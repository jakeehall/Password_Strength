#Jacob Hall
#Created: February 18th, 2016
#Password Strength v1.0
#Based on the website: http://www.passwordmeter.com
#paswords.txt found at: 
#GNU General Public License v3.0

import string
import getpass

class PasswordStrength():
    def __init__(self):
        print("Password Strength will determine how strong your password is.")
        self.passwordList = []
        try:
            fin = open("passwords.txt", 'r')
            for password in fin:
                if (password[0] != '#') and (password[1] != ' '):
                    self.passwordList.append(password.strip())
            fin.close()
        except FileNotFoundError as err:
            print(err + "\npasswords.txt not found!")
        self.getUsersPassword()

    def getUsersPassword(self):
        self.usersPassword = str(getpass.getpass("Please enter your password: "))
        if self.checkCommonPasswords():
            print("Score: 0%\nComplexity: \"Common Password\"")
        else:
            self.checkPasswordStrength()

    def checkCommonPasswords(self):#returns True if password matches common password
        self.passwordLength = len(self.usersPassword)
        for password in self.passwordList:
            if len(password) == self.passwordLength:#only looks at passwords that are the same length to save time
                for i in range(self.passwordLength):#compares each chr in the strings
                    if password[i] == self.usersPassword[i]:
                        if i == self.passwordLength-1:
                            return True
                    else:
                        break#if one chr doesnt compare it will break out of the loop
        return False

    def checkPasswordStrength(self):
        uppercaseChars = 0
        lowercaseChars = 0
        numberChars = 0
        symbolChars = 0
        middleNumbersAndSymbolsChars = 0
        for i in range(self.passwordLength):
            currentChar = self.usersPassword[i]
            if currentChar.isupper():
                uppercaseChars += 1
            elif currentChar.islower():
                lowercaseChars += 1
            elif currentChar.isdigit():#check if the current char in userPassword is a number
                numberChars += 1
                if (i != 0) and (i != self.passwordLength-1):
                    middleNumbersAndSymbolsChars += 1
            elif currentChar in string.punctuation:#checks if the current char in userPassword is a symbol
                symbolChars += 1
                if (i != 0) and (i != self.passwordLength-1):
                    middleNumbersAndSymbolsChars += 1

        #Additions to score
        requirementScore = 0
        lengthScore = self.passwordLength * 4
        if uppercaseChars > 0:
            uppercaseScore = (self.passwordLength-uppercaseChars)*2
            if uppercaseChars >= 1:
                requirementScore += 1
        else:
            uppercaseScore = 0
        if lowercaseChars > 0:
            lowercaseScore = (self.passwordLength-lowercaseChars)*2
            if lowercaseChars >= 1:
                requirementScore += 1
        else:
            lowercaseScore = 0
        numberScore = numberChars*4
        symbolScore = symbolChars*6
        middleNumbersAndSymbolsScore = middleNumbersAndSymbolsChars * 2
        if numberChars >= 1:
            requirementScore += 1
        if symbolChars >= 1:
            requirementScore += 1
        if (self.passwordLength < 8) or (requirementScore < 3):
            requirementScore = 0
        else:
            requirementScore += 1
        requirementScore = requirementScore * 2

        #Deductions from score
        allLettersScore = 0;
        allNumbersScore = 0;
        if self.usersPassword.isalpha():
            allLettersScore = -(self.passwordLength)
        if self.usersPassword.isdigit():
            allNumbersScore = -(self.passwordLength)
        
        
        
        #Total Score
        totalScore = lengthScore + uppercaseScore + lowercaseScore + numberScore + symbolScore + middleNumbersAndSymbolsScore + requirementScore + allLettersScore + allNumbersScore
        scoreComplexity = ""
        if totalScore > 100:
            totalScore = 100
        if totalScore < 20:
            scoreComplexity = "Very Weak"
        elif totalScore < 40:
            scoreComplexity = "Weak"
        elif totalScore < 60:
            scoreComplexity = "Good"
        elif totalScore < 80:
            scoreComplexity = "Strong"
        else:
            scoreComplexity = "Very Strong"
            
        #Print out users password strength information    
        print("ADDITIONS\nLength Score: ",lengthScore,"\nUppercase Score:",uppercaseScore,"\nLowercase Score:",lowercaseScore,"\nNumber Score:",numberScore,"\nSymbol Score:",symbolScore,"\nMiddle Numbers or Symbols Score:",middleNumbersAndSymbolsScore,"\nRequirement Score:",requirementScore,"\n")
        print("DEDUCTIONS\nLetters Only Score:",allLettersScore,"\nNumbers Only Score:",allNumbersScore,"\nRepatitive Character Score: 0\nConsecutive Uppercase Letters: 0\nConsecutive Lowercase Letters: 0\nConsecutive Numbers: 0\nSequential Letters (3+): 0\nSequential Numbers (3+): 0\nSequential Symbols (3+): 0\n")
        print("TOTAL\nScore:",totalScore,"%\nComplexity: \""+scoreComplexity+"\"\n")

PasswordStrength()
