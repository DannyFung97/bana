import time
import random

banfiv = False
hasItems = 0
work = 1
turn = 1
av_bananas = 50
stamina = 24
staminaBase = stamina
staminaCap = stamina
name = ""
max_due = 40
annual = 20
bus_cost = 5
first_turn_offset = False

item_array = [
    # item name, item count, item buy_price, item sell_price
    ["gold",   0, 1,  1],
    ["banana", 0, 15,  10],
    ["seed",   0, 35, 30],
    ["pill",   0, 50, 40]
]

arr = item_array

service_array = [
    # name, activation, bill turn due, fee, checking_account, savings_account
    ["Bank Service Fee", False, 0, 10, 0, 0],  # bank
    # name, activation, bill turn start, fee, funds, is_ill
    ["Health Care", False, 0, 20, 0, False],  # health care
    # name, activation, bill turn start, fee, claimed_funds
    ["Insurance", False, 0, 40, 0],  # insurance
    ["Rent", True, 0, 100, 0]  # rent
]

ser = service_array

loan_array = [False, 0, 0, 1, 0]

lo = loan_array
# loan exists, amount loaned, amount owed, interest rate a turn, turn due


def reset_game():
    global turn
    global stamina
    global staminaBase
    global staminaCap
    global hasItems
    global work
    global av_bananas
    global banfiv
    global arr
    global ser
    global lo
    global first_turn_offset

    banfiv = False
    turn = 1
    stamina = staminaBase
    staminaCap = stamina
    av_bananas = 50
    hasItems = 0
    work = 1
    arr = item_array
    ser = service_array
    lo = loan_array
    first_turn_offset = False
    start()


def finances(calculate_dues):
    global turn
    global first_turn_offset

    # if first turn, offset rent by annual turns
    if first_turn_offset is False:
        ser[3][2] += annual
        first_turn_offset = True
    if calculate_dues is False:
        # display
        print("Finances:\nGold: ", arr[0][1], "\n")
        c = 0
        if ser[0][1] is True:
            print("Bank Account: Checking: ", ser[0][4], " Gold, Savings: ", ser[0][5], " Gold.")
            if lo[0] is True:
                print("Loan: Borrowed: ", lo[1], ", Owed: ", lo[2], ", Interest: ", lo[3], "%, Turn Due: ", lo[4])
        while c < len(ser):
            if ser[c][1] is True:
                print(ser[c][3], " Gold due in ", ser[c][2] - turn, " turns for ", ser[c][0], ".")
            c += 1
    else:
        # savings
        ser[0][5] += ser[0][5] / (lo[3] * 100 * (4/3))
        ser[0][5] = round(ser[0][5], 2)
        # loans
        if lo[0] is True:
            lo[2] += lo[2] / (100/lo[3])
            lo[2] = round(lo[2], 2)
        if lo[4] == turn:
            if ser[0][4] >= lo[2]:
                ser[0][4] -= lo[2]
            else:
                arr[0][1] -= (lo[2] - ser[0][4])
                ser[0][4] = 0
        c = 0
        # insurance calculation
        if (ser[2][4] > 0) and ser[2][0] is True:
            print("You recently were a victim of thievery, ", ser[2][4], " Gold is given to you as compensation.")
            if ser[0][1] is True:
                ser[0][4] += ser[2][4]
            else:
                arr[0][1] += ser[2][4]
            ser[2][4] = 0
            time.sleep(1)
        # calculation and deduction of fees and bills
        while c < len(ser):
            if ser[c][1] is True:
                if ser[c][2] == turn:
                    print(ser[c][3], " Gold deducted from your account for ", ser[c][0], ".")
                    ser[c][2] += annual
                    if ser[0][4] >= ser[c][3]:
                        ser[0][4] -= ser[c][3]
                    else:
                        arr[0][1] -= (ser[c][3] - ser[0][4])
                        ser[0][4] = 0
                    if (c == 1) or (c == 2):
                        ser[c][4] += (ser[c][3] // 2)
            c += 1


def inventory(show_details):
    global hasItems
    q = 0
    c = 1

    if show_details is True:
        print("Inventory:\nGold: ", arr[0][1], "\n")
    while c < len(arr):
        q += arr[c][1]
        if show_details is True:
            print(arr[c][0], " - Owned: ", arr[c][1], " - Buy: ", arr[c][2], " - Sell: ", arr[c][3], "\n")
        c += 1
    hasItems = q


def wi():
    print("I don't know that input, let's try again.")
    time.sleep(1)


def start():
    global name

    print("Hello and welcome!")
    name = input("What's your name:")
    print("Welcome, " + name + "!")
    print("You play as a farmer with a field full of banana trees. Your goal is to have as much gold as possible.")
    print("After collecting the bananas you sell them.")
    choice = input("Do you want to play? A=Yes/S=No")
    if choice == "A":
        print("Let's get started!")
        finances(True)
        begin()
    if choice == "S":
        print("Okay, bye...")
    else:
        wi()
        start()


def begin():
    global stamina
    global av_bananas
    global turn
    global bus_cost
    if arr[0][1] > 999:
        print("You've Won the game! (", turn, " turns)")
        time.sleep(1)
        play = input("Do you want to play again? A=Yes/S=No")
        if play == "A":
            reset_game()
        if play == "S":
            print("Congrats again!")
        else:
            wi()
    if stamina < 1:
        if ser[0][1] is True:
            print("The clinic staff arrived and saved you from a horrible fate. (Stamina restored) (40 Gold lost)")
            stamina = staminaCap
            med_cost(40, False)
        else:
            print("You've lost the game due to starvation.")
            time.sleep(1)
            play = input("Do you want to play again? A=Yes/S=No")
            if play == "A":
                reset_game()
            else:
                print("Okay, bye...")
    if arr[0][1] < 0:
        print("You've lost the game due to financial loss.")
        time.sleep(1)
        play = input("Do you want to play again? A=Yes/S=No")
        if play == "A":
            reset_game()
        else:
            print("Okay, bye...")
    inventory(False)
    print("Turn: ", turn, "| Stamina: ", stamina, "/", staminaCap)
    option = input("What do you want to do now? A=Pick/S=Inventory/D=Market/F=Finances/G=Nothing")
    if option == "A":
        if av_bananas > 0:
            turn += 1
            print("You pick a banana.")
            arr[1][1] += 1
            stamina -= work
            av_bananas -= 1
            finances(True)
        else:
            print("There are no bananas to be picked.")
            time.sleep(1)
        begin()
    elif option == "S":
        inventory(True)
        time.sleep(1)
        if hasItems > 0:
            use()
        begin()
    elif option == "D":
        print("Take the bus(Bus cost: ", bus_cost, " Gold) or walk to the market?")
        to = input("A=Bus/S=Walk/D=Never Mind")
        if to == "A":
            if arr[0][1] >= bus_cost and arr[0][1] > 0:
                arr[0][1] -= bus_cost
                print("You take the bus...(Bus cost: ", bus_cost, " Gold)")
                time.sleep(3)
                if random.randint(0, 4) == 1:
                    traffic_jam(False, 0)
                else:
                    print("And made it!")
                time.sleep(1)
                market(True, False)
            else:
                print("You don't have enough money to take the bus!")
                time.sleep(1)
                begin()
        elif to == "S":
            if stamina >= work * 2:
                stamina -= work * 2
                print("You walked to the market...")
                time.sleep(3)
                if random.randint(0, 3) == 1:
                    bandit()
                else:
                    print("And made it!")
                time.sleep(1)
                market(True, False)
            else:
                print("You are too tired to walk!")
                time.sleep(1)
                begin()
        elif to == "D":
            begin()
        else:
            wi()
            begin()
    elif option == "F":
        finances(False)
        begin()
    elif option == "G":
        print("You spent the whole day doing nothing...(+2 stamina)")
        stamina += 2
        if stamina > staminaCap:
            stamina = staminaCap
        time.sleep(5)
        turn += 1
        finances(True)
        begin()
    else:
        wi()
        begin()


def bandit():
    global hasItems
    global banfiv

    print("A group of bandits stands in your way, and the leader speaks.")
    time.sleep(3)
    sce = random.randint(0, 6)
    if sce == 1:
        print("'Got any food you don't mind sharing with us?'")
        time.sleep(1)
        if arr[1][1] > 0:
            bandit_one(True)
    elif sce == 2:
        print("'You look like you have gold, pay up. 40 gold would be nice.'")
        time.sleep(1)
        if arr[0][1] > 0:
            bandit_two(True)
    elif sce == 3:
        print("'Hi!'")
        time.sleep(1)
        bandit_three()
    elif sce == 4:
        print("'Hey guys, let's beat 'em up!'")
        time.sleep(1)
        bandit_four()
    elif sce == 5:
        print("'What's your name?'")
        time.sleep(1)
        if banfiv is False:
            bandit_five(True, 0)
            banfiv = True
        else:
            print("'Oh wait, we've asked you already. Have a good day.'")
    else:
        print("'Give us everything and we will be on our way'.")
        time.sleep(1)
        bandit_option = input("What will you do? A=Ok/S=Run/D=Fight")
        if bandit_option == "A":
            c = 0
            while c < len(arr):
                arr[c][1] = 0
            hasItems = 0
            print("You gave the bandits everything.")
            time.sleep(1)
            print("'You're such a nice person, being so generous like this, thanks.', said the leader.")
        elif bandit_option == "S":
            run()
        elif bandit_option == "D":
            fight(True)
        else:
            "'You can't expect something good to happen by pressing some other key. Guys, weapons out.'"
            time.sleep(1)
            fight(False)
    time.sleep(1)
    print("Then the bandits left and you continued on to the market.")


def bandit_one(can_lie):
    if can_lie is True:
        bandit_option = input("What will you do? A=Lie/S=Spare some food/D=Run/F=Fight")
    else:
        bandit_option = input("What will you do? S=Spare some food/D=Run/F=Fight")
    if bandit_option == "A" and can_lie is True:
        print("You told them that you don't have any food on you.")
        time.sleep(1)
        dif = random.randint(0, 3)
        if dif == 1:
            print("'Oh okay, that's fine. Bye!'")
            time.sleep(1)
        if dif == 2:
            print("'You're a farmer, how do you not have food to spare?'")
            time.sleep(1)
            bandit_one(False)
        else:
            print("'Guys, go over and check.'")
            time.sleep(1)
            print("The bandits tramped through your personal space and searched your belongings...")
            time.sleep(1)
            if arr[1][1] > 0:
                exa = random.randint(0, 2)
                if exa == 1:
                    print("The bandits couldn't find any food in your belongings.")
                    time.sleep(1)
                    print("'Huh, well, have a good day then.', said the leader.")
                else:
                    print("The bandits found your bananas!")
                    fight(True)
    elif bandit_option == "S":
        if arr[1][1] >= 1 + (turn // 9) * 3:
            print("You gave them ", 1 + (turn // 9) * 3, " bananas.")
        arr[1][1] -= 1 + (turn // 9) * 3
        time.sleep(1)
        print("The leader and the bandits seemed satisfied.")
    elif bandit_option == "D":
        run()
    elif bandit_option == "F":
        fight(True)
    else:
        wi()
        bandit_one(can_lie)


def bandit_two(can_lie):
    if can_lie is True:
        bandit_option = input("What will you do? A=Lie/S=Pay Gold/D=Run/F=Fight")
    else:
        bandit_option = input("What will you do? S=Pay/D=Run/F=Fight")
    if bandit_option == "A" and can_lie is True:
        print("You told them you didn't have any gold.")
        time.sleep(1)
        dif = random.randint(0, 2)
        if dif == 1:
            print("'Come on, who do you take us for? You're obviously lying.'")
            time.sleep(1)
            bandit_two(False)
        if dif == 2:
            print("'Well that's fine, because we can just beat you for fun this time instead.', said the leader.")
            time.sleep(1)
            fight(True)
    elif bandit_option == "S":
        if arr[0][1] >= 40:
            arr[0][1] -= 40
            print("You gave them 40 Gold.")
            time.sleep(1)
            print("The bandits grinned at each other as they divided up the gold in front of you.")
        elif arr[0][1] > 0:
            arr[0][1] = 0
            print("You gave them what little gold you had.")
            time.sleep(1)
            print("The bandits seemed a bit mad when they saw the amount of gold, then they glared at you.")
            time.sleep(1)
            fight(False)
        else:
            print("You don't have any gold to give!")
            time.sleep(1)
            bandit_two(can_lie)
    elif bandit_option == "D":
        run()
    elif bandit_option == "F":
        fight(True)
    else:
        wi()
        bandit_two(can_lie)


def bandit_three():
    global stamina

    bandit_option = input("A=Uh...hi?")
    if bandit_option == "A":
        print("'I've just finished reciting a poem for a play tomorrow, want to hear it?', asked the leader.")
        time.sleep(1)
        bandit_option = input("A=Stay/S=I have to go...")
        if bandit_option == "S":
            print("You: 'Sorry, I have to go-'")
            time.sleep(.500)
        print("'Alright! Here we go!'")
        time.sleep(1)
        print("'Ahem...'")
        ti = 4
        time.sleep(ti)
        print("'Take all my loves, my love, yea, take them all:'")
        time.sleep(ti)
        print("'What hast thou then more than thou hadst before?'")
        time.sleep(ti)
        print("'No love, my love, that thou mayst true love call-'")
        time.sleep(ti)
        print("'All mine was thine before thou hadst this more.'")
        time.sleep(ti)
        print("'Then if for my love thou my love receivest,'")
        time.sleep(ti)
        print("'I cannot blame thee for my love thou usest;'")
        time.sleep(ti)
        print("'But yet be blamed if thou this self deceivest'")
        time.sleep(ti)
        print("'By wilful taste of what thyself refusest.'")
        time.sleep(ti)
        print("'I do forgive thy robb'ry, gentle thief,'")
        time.sleep(ti)
        print("'Although thou steal thee all my poverty;'")
        time.sleep(ti)
        print("'And yet love knows it is a greater grief'")
        time.sleep(ti)
        print("'To bear love's wrong than hate's known injury.'")
        time.sleep(ti)
        print("'Lascivious grace, in whom all ill well shows,'")
        time.sleep(ti)
        print("'Kill me with spites, yet we must not be foes.'")
        time.sleep(ti)
        print("'That was Sonnet 40 by William Shakespeare, so what did you think?'")
        time.sleep(1)
        bandit_option = input("A=Applaud/S=Boo")
        if bandit_option == "A":
            print("You applauded the leader, whose poem touched your heart and made your day. (Stamina restored)")
            stamina = staminaCap
            time.sleep(1)
            print("'T-thank you! Thank you very much! See, guys? Not everyone dislikes poetry!', said the leader.")
            time.sleep(1)
            print("The other bandits just looked at each other and lightly nodded at the leader's statement.")
        else:
            print("'...'")
            time.sleep(1)
            print("'Okay, I tried to be nice by sharing something and now I'm pissed; I'll beat you for that.'")
            time.sleep(1)
            fight(False)
    else:
        wi()
        bandit_three()


def bandit_four():
    fight(True)


def bandit_five(can_be_silent, stage):
    if stage <= 0:
        if can_be_silent is True:
            bo = input("What will you do? A=Say something/S=Stay silent")
        else:
            bo = input("What will you do? A=Say something")
        if bo == "A":
            bo = input("Enter your name: ")
            print("You told the leader that your name is ", bo, ". The leader took out a notepad and wrote something.")
        elif bo == "S":
            print("You stayed silent.")
            time.sleep(1)
            print("The leader squinted and asked you again, 'What is your name? I won't ask again.'")
            time.sleep(1)
            bandit_five(False, 0)
        else:
            wi()
            bandit_five(can_be_silent, 0)
        time.sleep(1)
        print("'What is your credit card number?'")
        time.sleep(1)
    if stage <= 1:
        bo = input("Enter your credit card number: ")
        if isinstance(int(bo), int) is not True:
            print("'That's not a number, idiot.'")
            time.sleep(1)
            bandit_five(False, 1)
    print("'And the CVV?'")
    time.sleep(1)
    if stage <= 2:
        bo = input("Enter the CVV for the aforementioned credit card number: ")
        if isinstance(int(bo), int) is not True:
            print("'No, again.'")
            time.sleep(1)
            bandit_five(False, 2)
    time.sleep(1)
    print("The leader nodded and asked, 'What is your age?'")
    time.sleep(1)
    if stage <= 3:
        bo = input("Enter your age: ")
        if isinstance(int(bo), int) is not True:
            print("'No, that's not your age.'")
            time.sleep(1)
            bandit_five(False, 3)
    time.sleep(1)
    print("And finally, what is your social security number?'")
    time.sleep(1)
    if stage <= 4:
        bo = input("Enter your social security number: ")
        if isinstance(int(bo), int) is not True:
            print("'No, that's obviously not a social security number.'")
            time.sleep(1)
            bandit_five(False, 4)
    time.sleep(1)
    print("'You've provided us much data.', said the leader.")
    time.sleep(1)
    print("'But the information you've entered could be fabricated, so it is not like we can use it.'")
    time.sleep(1)
    print("'Hey, relax! This game doesn't save any data so if you did say your actual info, then it is safe with us!'")
    time.sleep(1)
    print("Some of the bandits clapped, perhaps because of your cooperation.")


def traffic_jam(coming_back, tr):
    global stamina
    global staminaCap

    print("There is a traffic jam!")
    time.sleep(1)
    if tr == 0:
        tr = hows_traffic()
    time.sleep(1)
    wait_option = input("Would you like to walk the rest of the way or stay on the bus? A=Walk/S=Stay")
    if wait_option == "A":
        if coming_back is True:
            print("You've made it back home.")
            stamina -= work
            print("(", stamina, "/", staminaCap, ")")
            begin()
        else:
            print("You walked and made it to the market , but you feel more tired.")
            stamina -= work
            print("(", stamina, "/", staminaCap, ")")
            market(True, False)
    elif wait_option == "S":
        print("You stayed on the bus and waited...")
        t = random.randint(4, 15) * tr
        time.sleep(t)
        if coming_back is True:
            print("You've arrived home!")
            time.sleep(1)
            begin()
        else:
            print("You've arrived to the market!")
            time.sleep(1)
            market(True, False)
    else:
        wi()
        traffic_jam(coming_back, tr)


def run():
    global stamina
    global staminaCap
    global hasItems

    time.sleep(1)
    print("You ran the other way...")
    time.sleep(1)
    print("You found a bush nearby and hid in it, hoping the bandits won't find you.")
    time.sleep(1)
    rch = (stamina*100 - (hasItems - arr[0][1])*10) // staminaCap
    if rch <= 40:
        print("But the bandits grabbed you out of the bush and beat you up.")
        time.sleep(1)
        if hasItems > 0:
            print("They also took some of your belongings.")
            c = 0
            while c < len(arr):
                if ser[2][1] is True:
                    ser[2][4] += ((arr[c][1] // (3/2)) * arr[c][2])
                arr[c][1] //= (3/2)
                c += 1
            time.sleep(1)
    else:
        print("Through the bush, you saw bandits looking around for you.")
        print("(Run cost one stamina)")
    stamina -= work
    time.sleep(1)


def fight(first_time):
    global stamina
    global staminaCap

    if first_time is True:
        time.sleep(1)
        print("You rose your fists against the bandits, and in return, the leader and the bandits rose theirs as well.")
    time.sleep(1)
    rch = (stamina*100) // staminaCap
    if rch <= 45:
        print("The bandits beat you up.")
        time.sleep(1)
        if hasItems > 0:
            print("They also took some of your belongings.")
            c = 0
            while c < len(arr):
                if ser[2][1] is True:
                    ser[2][4] += ((arr[c][1] // (3/2)) * arr[c][2])
                arr[c][1] //= 2
                c += 1
            time.sleep(1)
    else:
        print("You held your ground against the bandits' blows until they gave up.")
        print("(Fight cost one stamina)")
    stamina -= work
    time.sleep(1)


def hows_traffic():
    jam = random.randint(0, 10)
    if jam < 5:
        print("It doesn't look that bad.")
        return 1
    elif jam < 8:
        print("It looks sort of bad.")
        return 2
    elif jam < 10:
        print("This looks bad.")
        return 3
    else:
        print("Wow, it looks really bad...")
        return 4


def use():
    use_option = input("Which item would you like to use? A=Banana/S=Seed/D=Pill/F=None")
    if use_option == "A":
        eat()
    elif use_option == "S":
        seed()
    elif use_option == "D":
        pill()
    elif use_option == "F":
        begin()
    else:
        wi()
        use()


def eat():
    global stamina
    global staminaCap
    global turn

    if arr[1][1] > 0:
        print("You ate a banana...")
        arr[1][1] -= 1
        stamina = stamina + 4
        if stamina > staminaCap:
            stamina = staminaCap
        if random.randint(0, 2) == 1:
            print("You found a seed!")
            arr[2][1] += 1
        time.sleep(1)
        finances(True)
    else:
        print("You have no bananas to eat!")
        time.sleep(1)
    use()


def seed():
    global av_bananas
    global stamina
    global turn

    if arr[2][1] > 0:
        print("You attempt to plant a seed...")
        turn += 1
        arr[2][1] -= 1
        stamina -= work
        time.sleep(1)
        tr = random.randint(0, 6)
        if tr == 1:
            print("The seed grew into a splendid banana tree! (+8 available bananas)")
            av_bananas += 8
        elif tr > 4:
            print("But nothing happened.")
        else:
            print("The seed grew into a banana tree! (+4 available bananas)")
            av_bananas += 4
        finances(True)
    else:
        print("You have no seeds to plant!")
    time.sleep(1)
    use()


def pill():
    global staminaCap
    global stamina
    global work
    global turn

    if arr[3][1] > 0:
        print("You consumed the pill...")
        turn += 1
        arr[3][1] -= 1
        time.sleep(1)
        if random.randint(0, 3) != 1:
            print("You feel much better.")
            staminaCap += 8
            stamina = staminaCap
            work += 1
        else:
            print("But nothing happened.")
        finances(True)
    else:
        print("You have no pills!")
    time.sleep(1)
    use()


def market(visiting, still_at_market):
    global stamina
    global work
    global turn
    global bus_cost

    if visiting is True:
        if still_at_market is True:
            print("You're still at the market.")
        else:
            print("Welcome to the market!")
        time.sleep(1)
        trade()
    else:
        print("Thank you! Please come back soon!")
        time.sleep(1)
        print("Take the bus(Bus cost: ", bus_cost, " Gold) or walk home?")
        travel_option = input("A=Bus/S=Walk/D=Never Mind")
        if travel_option == "A":
            if arr[0][1] >= bus_cost and arr[0][1] > 0:
                arr[0][1] -= bus_cost
                print("You take the bus back home...")
                time.sleep(3)
                if random.randint(0, 4) == 1:
                    traffic_jam(True, 0)
                else:
                    print("And made it!")
                time.sleep(1)
                turn += 1
                finances(True)
                begin()
            else:
                print("You don't have enough money to take the bus!")
                time.sleep(1)
                market(True, True)
        elif travel_option == "S":
            if stamina >= work * 2:
                stamina -= work * 2
                print("You walked back home...")
                time.sleep(3)
                if random.randint(0, 4) == 1:
                    bandit()
                else:
                    print("And made it!")
                time.sleep(1)
                turn += 1
                finances(True)
                begin()
            else:
                print("You are too tired to walk!")
                time.sleep(1)
                market(True, True)
        elif travel_option == "D":
            trade()
        else:
            wi()
            market(visiting, still_at_market)


def trade():
    inventory(True)
    trade_option = input("Would you like to do here at the market? A=Buy/S=Sell/D=Service Center/F=Leave")
    if trade_option == "A":
        buy()
    elif trade_option == "S":
        sell()
    elif trade_option == "D":
        print("Welcome to the Service Center!")
        time.sleep(1)
        services()
    elif trade_option == "F":
        market(False, True)
        begin()
    else:
        wi()
        trade()


def buy():
    global i

    buy_option = input("What would you like to buy? A=Banana/S=Seed/D=Pill/F=Never Mind")
    if buy_option == "A":
        i = 1
    elif buy_option == "S":
        i = 2
    elif buy_option == "D":
        i = 3
    elif buy_option == "F":
        trade()
    else:
        wi()
        buy()
    amount_o = input("How many would you like to buy? A=Some Amount.../S=Never Mind")
    if amount_o == "A":
        amount = input("Enter amount you want to buy: ")
        b = ""
        if int(amount) > 1:
            b = "s"
        if arr[0][1] >= arr[i][2] * int(amount):
            time.sleep(1)
            arr[0][1] = arr[0][1] - arr[i][2] * int(amount)
            print("You bought ", amount, " ", arr[i][0], b, ". You have ", arr[0][1], " gold left.")
            arr[i][1] = arr[i][1] + int(amount)
            time.sleep(1)
            buy()
        if ser[0][4] >= arr[i][2] * int(amount):
            time.sleep(1)
            ser[0][4] = ser[0][4] - (ser[0][3]/2) - arr[i][2] * int(amount)
            print("You bought ", amount, " ", arr[i][0], b, " via Checking Account. (", ser[0][3]/2, " Gold surcharge)")
            print("You have ", ser[0][4], " gold left in your account.")
            arr[i][1] = arr[i][1] + int(amount)
            time.sleep(1)
            buy()
        else:
            print("You don't have enough gold.")
            buy()
    elif amount_o == "S":
        trade()
    else:
        wi()
        buy()


def sell():
    global i

    sell_option = input("What would you like to sell? A=Bananas/S=Seeds/D=Pills/F=Never Mind")
    if sell_option == "A":
        i = 1
    elif sell_option == "S":
        i = 2
    elif sell_option == "D":
        i = 3
    elif sell_option == "F":
        trade()
    else:
        wi()
        sell()
    amount = input("How many would you like to sell? A=All/S=Some Amount.../D=Never Mind")
    if arr[i][1] > 0:
        if amount == "A":
            arr[0][1] = arr[0][1] + arr[i][1] * arr[i][3]
            print("You sold all your ", arr[i][0], "s and received ", arr[i][1] * arr[i][3], " gold")
            arr[i][1] = 0
            time.sleep(1)
            sell()
        elif amount == "S":
            b = ""
            so = input("Enter amount to sell: ")
            am = int(so)
            if am > 1:
                b = "s"
            if am > arr[i][1]:
                am = arr[i][1]
            arr[i][1] = arr[i][1] - am
            arr[0][1] = arr[0][1] + arr[i][3] * am
            print("You sold ", am, " ", arr[i][0], b, " (", arr[i][1], " left) and got ", arr[i][3] * am, " gold")
            time.sleep(1)
            sell()
        elif amount == "D":
            sell()
        else:
            wi()
            sell()
    else:
        print("You have no ", arr[i][0], "s to sell.")
        time.sleep(1)
        sell()


def services():
    o = input("Where would you like to go? A=Bank/S=Healthcare/D=Insurance/F=Finances/G=Market")
    if o == "A":
        print("Welcome to the Bank!")
        time.sleep(1)
        bank()
    elif o == "S":
        print("Welcome to the Health Care Clinic!")
        time.sleep(1)
        care()
    elif o == "D":
        insurance()
    elif o == "F":
        finances(False)
        services()
    elif o == "G":
        market(True, False)
    else:
        wi()
        services()


def bank():
    global turn

    if ser[0][1] is False:
        o = input("What would you like to do at the bank? A=Open a new account/S=More info/D=Service Center")
        if o == "A":
            print("Opening a new account requires an initial fee of ", ser[0][3] * 3, " Gold, proceed?")
            o = input("A=Yes/S=No")
            if o == "A":
                if arr[0][1] >= (ser[0][3] * 3):
                    arr[0][1] -= (ser[0][3] * 3)
                    ser[0][1] = True
                    time.sleep(1)
                    print("Congratulations! You now have access to the bank's services.")
                    ser[0][2] = (turn + annual)
                else:
                    print("You don't have enough gold.")
                time.sleep(1)
                bank()
            else:
                bank()
        elif o == "S":
            time.sleep(1)
            bmoi()
            bank()
        elif o == D":
            print("Welcome to the Service Center!")
            time.sleep(1)
            services()
        else:
            wi()
            bank()
    else:
        o = input("What would you like to do at the bank? A=Gold Storage/S=Loans/D=More Info/F=Cancel/G=Service Center")
        if o == "A":
            print("Checking: ", ser[0][4], " | Savings: ", ser[0][5], " | Self: ", arr[0][1], " Gold")
            o = input("A=Deposit/S=Withdraw/D=Never Mind")
            if o == "A":
                o = input("Enter amount of gold you want to deposit: ")
                dep = int(o)
                if dep > arr[0][1]:
                    dep = arr[0][1]
                oo = input("Where would you like to deposit into? A=Checking/S=Savings")
                if oo == "A":
                    arr[0][1] -= dep
                    ser[0][4] += dep
                    print("You have deposited ", dep, " Gold into your Checking account.")
                elif oo == "S":
                    arr[0][1] -= dep
                    ser[0][5] += dep
                    print("You have deposited ", dep, " Gold into your Savings account.")
                else:
                    wi()
                    bank()
                time.sleep(1)
                bank()
            elif o == "S":
                o = input("Enter amount of gold you want to withdraw: ")
                wit = int(o)
                oo = input("Where would you like to withdraw from? A=Checking/S=Savings")
                if oo == "A":
                    if wit > ser[0][4]:
                        wit = ser[0][4]
                    ser[0][4] -= wit
                    arr[0][1] += wit
                    print("You have withdrawn ", wit, " Gold from your Checking account.")
                elif oo == "S":
                    if wit > ser[0][5]:
                        wit = ser[0][5]
                    ser[0][5] -= wit
                    arr[0][1] += wit
                    print("You have withdrawn ", wit, " Gold from your Savings account.")
                else:
                    wi()
                    bank()
                time.sleep(1)
                bank()
            else:
                bank()
        elif o == "S":
            loan()
        elif o == "D":
            time.sleep(1)
            bmoi()
            bank()
        elif o == "F":
            o = input("Cancel bank service? If you want to open a new account later, fees are doubled. A=Yes/S=No")
            if o == "A":
                if lo[0] is True:
                    time.sleep(1)
                    print("You still have a loan to repay. You cannot cancel right now.")
                    time.sleep(1)
                    bank()
                else:
                    ser[0][1] = False
                    arr[0][1] += (ser[0][4] + int(ser[0][5]))
                    ser[0][4] = 0
                    ser[0][5] = 0
                    ser[0][2] *= 2
                    time.sleep(1)
                    print("Gold from your accounts have been transferred to you as you are no longer using the bank.")
                    print("Thank you for experiencing the provided services of our bank. We hope to see you again.")
                    time.sleep(1)
                    bank()
            elif o == "S":
                bank()
            else:
                wi()
                bank()
        elif o == "G":
            services()
        else:
            wi()
            bank()


def bmoi():
    print("The bank offers you financial security through loans, gold storage, and protected payments.")
    print("Whenever you borrow gold from the bank, you will have ", max_due, " turns to repay it along with ")
    print("interest (", lo[3], "%) a turn. When storing gold in the bank, you may store in the Checking ")
    print("or the Savings account. If you have gold in the Checking account, it can be used for more secure ")
    print("transactions. When paying, gold is drawn from your Checking account first, and then from your ")
    print("personal gold. If you have gold in your Savings account, the gold will grow at the rate of ")
    print(lo[3] * (3/4), "%, Gold in your Savings account cannot be used in secure transactions. In exchange for this")
    print(" service, you are required to pay a maintenance fee of ", ser[0][3], " Gold per ", annual, " turns.")
    print("When doing certain transactions, the gold will be taken out of your checking account before taken from your")
    print("person. If you cancel our services, all stored gold return to your person.")


def loan():
    global name

    if lo[0] is True:
        print("Gold on Self: ", arr[0][1], " | Gold in Storage: ", ser[0][4] + ser[0][5])
        print("Loan | Borrowed: ", lo[1], " Owed: ", lo[2], " Interest Per Turn: ", lo[3], "% Turn Due: ", lo[4])
        time.sleep(1)
        o = input("Would you like to repay your current loan? A=Yes/S=No")
        if o == "A":
            if arr[0][1] + ser[0][4] >= lo[2]:
                if ser[0][4] >= lo[2]:
                    ser[0][4] -= lo[2]
                    ser[0][4] = int(ser[0][4])
                else:
                    arr[0][1] -= (lo[2] - ser[0][4])
                    arr[0][1] = int(arr[0][1])
                    ser[0][4] = 0
                time.sleep(1)
                print("Loan debt resolved, thank you.")
                lo[0] = False
                lo[4] = 0
            else:
                print("You don't own enough gold to repay the loan.")
            time.sleep(1)
            bank()
        else:
            bank()
    else:
        print("Would you like to borrow a loan? (", lo[3], "% Interest Per Turn, Due Turn ", turn + max_due, ")")
        o = input("A=Yes/S=No")
        if o == "A":
            ln = input("Enter loan amount: ")
            print("The bank loans you ", int(ln), " Gold with ", lo[3], "% interest per turn.")
            print("If the amount is not repaid by Turn ", turn + max_due,
                  ", the bank will have no choice but to take legal action against you.")
            o = input("If you, the borrower, acknowledge the condition of this agreement, please sign your name: ")
            if o == name:
                time.sleep(1)
                lo[0] = True
                lo[1] = int(ln)
                lo[2] = lo[1]
                lo[4] = turn + max_due
                print("You have received a loan of ", lo[1], " Gold, it is placed in your checking account.")
                ser[0][4] += lo[1]
            else:
                time.sleep(1)
                print("Your signature does not match your real name, please confirm and try again.")
            time.sleep(1)
            bank()
        else:
            bank()


def care():
    global stamina
    global staminaCap
    global staminaBase
    global work

    if ser[1][1] is False:
        o = input("What would you like to do at the clinic? A=Open new account/S=Massage/D=More info/F=Service Center")
        if o == "A":
            print("Opening a new account requires an initial fee of ", (ser[1][3] // (2/3)), " Gold, proceed?")
            o = input("A=Yes/S=No")
            if o == "A":
                if arr[0][1] + ser[0][4] >= (ser[1][3] // (2/3)):
                    if ser[0][4] >= (ser[1][3] // (2/3)):
                        ser[0][4] -= (ser[1][3] // (2/3))
                    else:
                        arr[0][1] -= ((ser[1][3] // (2/3)) - ser[0][4])
                        ser[0][4] = 0
                    ser[1][1] = True
                    time.sleep(1)
                    print("Congratulations! You now have access to the clinic's services.")
                    ser[1][2] = (turn + annual)
                else:
                    print("You don't have enough gold.")
                time.sleep(1)
                care()
            else:
                care()
        elif o == "S":
            if stamina >= staminaCap:
                print("You don't feel like you need a massage.")
                time.sleep(1)
                care()
            print("Your stamina is at ", stamina, "/", staminaCap, ". Gold cost: ", 2 * (staminaCap - stamina))
            massage_cost = 2 * (staminaCap - stamina)
            o = input("Proceed with massage? A=Yes/S=No")
            if o == "S":
                care()
            elif o == "A":
                if arr[0][1] + ser[0][4] + ser[1][4] >= massage_cost:
                    med_cost(massage_cost, True)
                    time.sleep(1)
                    stamina = staminaCap
                    print("Your stamina has been restored.")
                    time.sleep(1)
                    care()
                else:
                    print("You don't have enough gold for a message.")
                    time.sleep(1)
                    care()
            else:
                wi()
                care()
        elif o == "D":
            time.sleep(1)
            cmoi()
            care()
        elif o == "F":
            print("Welcome to the Service Center!")
            time.sleep(1)
            services()
        else:
            wi()
            care()
    else:
        o = input("What would you like to do at the clinic? A=Treatment/S=More Info/D=Cancel/F=Service Center")
        if o == "A":
            o = input("What kind of treatment do you request? A=Massage/S=Drug Rehabilitation/D=Cure/F=Never Mind")
            if o == "A":
                if stamina >= staminaCap:
                    print("You don't feel like you need a massage.")
                    time.sleep(1)
                    care()
                print("Your stamina is at ", stamina, "/", staminaCap, ". Gold cost: ", 2 * (staminaCap - stamina))
                massage_cost = 2 * (staminaCap - stamina)
                o = input("Proceed with massage? A=Yes/S=No")
                if o == "S":
                    care()
                elif o == "A":
                    if arr[0][1] + ser[0][4] + ser[1][4] >= massage_cost:
                        med_cost(massage_cost, True)
                        time.sleep(1)
                        stamina = staminaCap
                        print("Your stamina has been restored.")
                        time.sleep(1)
                        care()
                    else:
                        print("You don't have enough gold for a message.")
                        time.sleep(1)
                        care()
                else:
                    wi()
                    care()
            elif o == "S":
                if work <= 1:
                    print("You don't feel like you need rehabilitation.")
                    time.sleep(1)
                    care()
                else:
                    print("You are signing up for drug rehabilitation...")
                    time.sleep(1)
                    a = (staminaCap - staminaBase) / 8
                    rehab_cost = int(10 + ((a * (a + 1)) / 2) * 5)
                    print("Cost of rehabilitation program is: ", rehab_cost, " Gold.")
                    o = input("Proceed? A=Yes/S=No")
                    if o == "A":
                        if arr[0][1] + ser[0][5] + ser[1][4] >= rehab_cost:
                            med_cost(rehab_cost, False)
                            work = 1
                            time.sleep(1)
                            print("Program completed, you no longer show symptoms of fatigue resulting from drugs.")
                            time.sleep(1)
                            print("Remember! Stay away from drugs!")
                        else:
                            print("You don't have enough gold.")
                        time.sleep(1)
                        care()
                    elif o == "S":
                        care()
                    else:
                        wi()
                        care()
            elif o == "D":
                if ser[1][5] is True:
                    print("You appear to have an illness, luckily we have a cure to that for ", ser[1][3] * 3, " Gold.")
                    o = input("Proceed? A=Yes/S=No")
                    if o == "A":
                        if arr[0][1] + ser[0][5] + ser[1][4] >= ser[1][3] * 3:
                            med_cost(ser[1][3] * 3, False)
                            ser[1][5] = False
                            time.sleep(1)
                            print("You feel better now thanks to the cure.")
                        else:
                            print("You don't own enough gold.")
                    elif o == "S":
                        care()
                    else:
                        wi()
                        care()
                else:
                    print("You don't appear to have an illness.")
                time.sleep(1)
                care()
        elif o == "S":
            time.sleep(1)
            cmoi()
            care()
        elif o == "D":
            o = input("Cancel clinic service? A=Yes/S=No")
            if o == "A":
                ser[1][1] = False
                time.sleep(1)
                print("Thank you for experiencing the provided services of our clinic. We hope to see you again.")
                time.sleep(1)
                care()
            elif o == "S":
                care()
            else:
                wi()
                care()
        elif o == "F":
            services()
        else:
            wi()
            care()


# med funds then personal gold then checking account or savings account
def med_cost(cost, from_checking):
    if ser[1][4] >= cost:
        ser[1][4] -= cost
    elif arr[0][1] >= cost:
        arr[0][1] -= cost
        ser[1][4] = 0
    elif (ser[0][4] >= cost) or (ser[0][5] >= cost):
        if from_checking is True:
            ser[0][4] -= cost
        else:
            ser[0][5] -= cost
        arr[0][1] = 0
        ser[1][4] = 0


def cmoi():
    print("The Health Care Clinic offers services concerning your stamina and overall health. Even if you don't have ")
    print("an account with us, you are still able to take a massage with us as you would otherwise. We would charge ")
    print("you 2 gold for every stamina we help restore. If you are taking drugs such as pills to boost your energy, ")
    print("you could show symptoms of long-term fatigue resulting from those drugs; you will become more and more ")
    print("tired if you keep taking drugs. With us, you can sign up for our rehabilitation program. Costs vary ")
    print("depending on your exposure to drugs. If you ever encounter an illness that is constantly draining you, we ")
    print("have a cure for that at the gold cost of ", ser[1][3] * 3, ". After opening an account with us at the ")
    print("initial fee of ", (ser[1][3] // (2 / 3)), " Gold, you will pay ", ser[1][3], " Gold every ", annual)
    print("turns, and in doing so, we place half of that amount into your Health Care account, which will accompany ")
    print("you in our future transactions; gold will be taken from your account with our clinic, then your person, ")
    print("and lastly your Savings account if you have a bank account. If you cancel our service, the gold you've ")
    print("been paying us every ", annual, " turns will remain for when you come back.")


def insurance():
    if ser[2][1] is False:
        o = input("What would you like to do at the agency? A=Open a new account/S=More info/D=Service Center")
        if o == "A":
            o = input("Create new account? A=Yes/S=No")
            if o == "A":
                ser[2][1] = True
                time.sleep(1)
                print("You have created an account, you now have access to our service.")
                ser[2][2] = (turn + annual)
                time.sleep(1)
                insurance()
            elif o == "S":
                insurance()
            else:
                wi()
                insurance()
        elif o == "S":
            time.sleep(1)
            imoi()
            insurance()
        elif o == "D":
            services()
        else:
            wi()
            insurance()
    else:
        o = input("What would you like to do at the agency? A=Cancel/S=More info/D=Service Center")
        if o == "A":
            o = input("Cancel our service? If you make a new account with us, fees are doubled. A=Yes/S=No")
            if o == "A":
                ser[2][1] = False
                ser[2][4] = 0
                ser[2][3] += 2
                time.sleep(1)
                print("You have cancelled your account, you will no longer have access to our service.")
                time.sleep(1)
                insurance()
            elif o == "S":
                insurance()
            else:
                wi()
                insurance()
        elif o == "S":
            time.sleep(1)
            imoi()
            insurance()
        elif o == "D":
            services()
        else:
            wi()
            insurance()


def imoi():
    print("This insurance company compensates you with gold in case of an accidental loss of assets or properties.")
    print("There is no initial fee to pay for a new account, but you will still need to pay ", ser[2][3], " Gold per")
    print(annual, " turns. In the case you have lost property, such as having your items stolen or destroyed, the ")
    print("company will send you gold equal to sum of the buying prices of all items in question. If you cancel ")
    print("service with us, fees are doubled the next time you sign up with us.")


start()
