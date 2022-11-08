import SetUpScreen
import AShadeDifferent

#Run the set up screen
setUpScreen = SetUpScreen.SetUp()
boardsetup = setUpScreen.Run()
game = AShadeDifferent.AShadeDifferent(boardsetup)
#Restart the board if the restart button was pressed
while game.Run() == True:
    game = AShadeDifferent.AShadeDifferent(boardsetup)