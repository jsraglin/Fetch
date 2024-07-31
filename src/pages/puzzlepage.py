#import unittest
from seleniumpagefactory import PageFactory
from selenium import webdriver
import time
class PuzzlePage(PageFactory):
    def __init__(self,driver):
        self.driver=driver

# Locators use ID where possible, but since the results button has ID='Reset'
# both of those elements needed full trimmed XPATHs to locate. Similarly, the
# Weighings list does not have an ID to again an XPATH was needed.
    locators = {
        "ResetButton": ('XPATH', "//*[@class='game']/div[4]/button[@id='reset']"),
        "WeighButton": ('ID', 'weigh'),
        "Right1": ('ID', 'right_0'),
        "Right2": ('ID', 'right_1'),
        "Right3": ('ID', 'right_2'),
        "Right4": ('ID', 'right_3'),
        "Right5": ('ID', 'right_4'),
        "Right6": ('ID', 'right_5'),
        "Right7": ('ID', 'right_6'),
        "Right8": ('ID', 'right_7'),
        "Right9": ('ID', 'right_8'),
        "Left1": ('ID', 'left_0'),
        "Left2": ('ID', 'left_1'),
        "Left3": ('ID', 'left_2'),
        "Left4": ('ID', 'left_3'),
        "Left5": ('ID', 'left_4'),
        "Left6": ('ID', 'left_5'),
        "Left7": ('ID', 'left_6'),
        "Left8": ('ID', 'left_7'),
        "Left9": ('ID', 'left_8'),
        "Coin0": ('ID', 'coin_0'),
        "Coin1": ('ID', 'coin_1'),
        "Coin2": ('ID', 'coin_2'),
        "Coin3": ('ID', 'coin_3'),
        "Coin4": ('ID', 'coin_4'),
        "Coin5": ('ID', 'coin_5'),
        "Coin6": ('ID', 'coin_6'),
        "Coin7": ('ID', 'coin_7'),
        "Coin8": ('ID', 'coin_8'),
        "Results": ('XPATH', "//*[@class='result']/button[@id='reset']"),
        "Weighings": ('XPATH', "//*[@class='game-info']/ol"),
        "Weighing1": ('XPATH', "//*[@class='game-info']/ol/li[1]"),
        "Weighing2": ('XPATH', "//*[@class='game-info']/ol/li[2]")
    }

    def LeftEntry(self,box,value):
        match box:
            case 1:
                self.Left1.set_text(str(value))
            case 2:
                self.Left2.set_text(str(value))
            case 3:
                self.Left3.set_text(str(value))
            case 4:
                self.Left4.set_text(str(value))
            case 5:
                self.Left5.set_text(str(value))
            case 6:
                self.Left6.set_text(str(value))
            case 7:
                self.Left7.set_text(str(value))
            case 8:
                self.Left8.set_text(str(value))
            case 9:
                self.Left9.set_text(str(value))
    def RightEntry(self,box,value):
        match box:
            case 1:
                self.Right1.set_text(str(value))
            case 2:
                self.Right2.set_text(str(value))
            case 3:
                self.Right3.set_text(str(value))
            case 4:
                self.Right4.set_text(str(value))
            case 5:
                self.Right5.set_text(str(value))
            case 6:
                self.Right6.set_text(str(value))
            case 7:
                self.Right7.set_text(str(value))
            case 8:
                self.Right8.set_text(str(value))
            case 9:
                self.Left9.set_text(str(value))
    def ClickGuess(self,guess):
        match guess:
            case 0:
                self.Coin0.click()
            case 1:
                self.Coin1.click()
            case 2:
                self.Coin2.click()
            case 3:
                self.Coin3.click()
            case 4:
                self.Coin4.click()
            case 5:
                self.Coin5.click()
            case 6:
                self.Coin6.click()
            case 7:
                self.Coin7.click()
            case 8:
                self.Coin8.click()
    def ClickWeigh(self):
        self.WeighButton.click()

    def ClickReset(self):
        self.ResetButton.click()
#In the case with arbitrary numbers of coins this could be generalized more    
    def GetFirstWeighing(self):
        return self.Weighing1.get_text()
    
    def GetSecondWeighing(self):
        return self.Weighing2.get_text()

    def GetResult(self):
        r=self.Results.get_text()
        return r
                
def test1():
    # The algorithm used to solve the puzzle is simple: divide the coins into
    # three equal piles, weigh two of them against each other.  This will narrow
    # the counterfeit's number down to one of those three piles, the lighter one
    # or the unweighed one if the two are equal.  Repeat the process until
    # a single coin is identified as counterfeit. This will find the coin in
    # ceiling(log n base 3) steps, two steps in the case here where n=9

    driver=webdriver.Chrome()
    driver.implicitly_wait(20)
    driver.get(url="http://sdetchallenge.fetch.com/")
    pggame=PuzzlePage(driver)
    pggame.LeftEntry(1,0)
    pggame.LeftEntry(2,1)
    pggame.LeftEntry(3,2)
    pggame.RightEntry(1,3)
    pggame.RightEntry(2,4)
    pggame.RightEntry(3,5)
    pggame.ClickWeigh()
    w1=pggame.GetFirstWeighing()
    # The Result button does not change until after the weighing has been updated,
    # So I get the newest weighing line to force an implicit wait that will
    # ensure that the Result button has been updated.
    res=pggame.GetResult()
    if (res=='='):
        possible=[6,7,8]
    elif (res=='>'):
        possible=[3,4,5]
    else:
        possible=[0,1,2]
    pggame.ClickReset()
    pggame.LeftEntry(1,possible[0])
    pggame.RightEntry(1,possible[1])
    pggame.ClickWeigh()
    w2=pggame.GetSecondWeighing()
    res2=pggame.GetResult()
    if (res2=='='):
        pggame.ClickGuess(possible[2])
    elif (res2=='>'):
        pggame.ClickGuess(possible[1])
    else:
        pggame.ClickGuess(possible[0])
    alertframe=driver.switch_to.alert
    Wintext=alertframe.text
    alertframe.dismiss()
    print("Test Results:")
    print("Alert output: {}".format(Wintext))
    print("Number of weighings: 2")
    print("Weighings: {}, {}".format(w1,w2))
def main():
    test1()

if __name__ == "__main__":
    main()