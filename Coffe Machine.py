class coffeeMachine:

    def __init__(self, ml_water, ml_milk, g_bens, nr_cups, money):
        self.ml_water = ml_water
        self.ml_milk = ml_milk
        self.g_beans = g_bens
        self.nr_cups = nr_cups
        self.money = money

    def resources_verification(self, resources):
        if self.ml_milk == 0:
            x = min(resources.ml_water/self.ml_water, resources.g_beans / self.g_beans, resources.nr_cups / self.nr_cups)
        else:
            x = min(resources.ml_water/self.ml_water, resources.ml_milk / self.ml_milk, resources.g_beans / self.g_beans, resources.nr_cups / self.nr_cups)
        if x > 1:
            print("I have enough resources, making you a coffee!")                
        elif resources.ml_water / self.ml_water < 1:
            print("Sorry, not enough water!")
            coffeeMachine.choose_your_action()
        elif resources.ml_milk / self.ml_milk < 1:
            print("Sorry, not enough water!")
            coffeeMachine.choose_your_action()
        elif resources.g_beans / self.g_beans < 1:
            print("Not enough coffe beans!")
            coffeeMachine.choose_your_action()
        else:
            print("Not enough disposal cups!")
            coffeeMachine.choose_your_action()

    def remaining_resources(self,resources): 
        resources.ml_water -= self.ml_water
        resources.ml_milk -= self.ml_milk
        resources.g_beans -= self.g_beans
        resources.nr_cups -= self.nr_cups
        resources.money += self.money

    def fill(resources):
        fill_water = int(input("\nWrite how many ml of water do you want to add:\n"))
        fill_milk = int(input('Write how many ml of milk do you want to add:\n'))
        fill_coffe_beans = int(input("Write how many grams of coffee beans do you want to add:\n"))
        fill_cups = int(input("Write how many disposable cups of coffee do you want to add:\n"))
        resources.ml_water += fill_water
        resources.ml_milk += fill_milk
        resources.g_beans += fill_coffe_beans
        resources.nr_cups += fill_cups
    
    def print_remaining():
        print(f"""\nThe coffee machine has:\n"""
f"""{resources.ml_water} of water\n"""
f"""{resources.ml_milk} of milk\n"""
f"""{resources.g_beans} of coffee beans\n"""
f"""{resources.nr_cups} of disposable cups\n"""
f"""${resources.money} of money""")

    def coffee_choice(espresso, latte, cappucino, resources):
        coffee_choice = input('\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
        if coffee_choice == '1':
            espresso.resources_verification(resources)   
            espresso.remaining_resources(resources)
        elif coffee_choice == '2':
            latte.resources_verification(resources) 
            latte.remaining_resources(resources)
        elif coffee_choice == '3':
            cappucino.resources_verification(resources) 
            cappucino.remaining_resources(resources)
        else:
            coffeeMachine.choose_your_action()

    def choose_your_action():
        while True:
            action = input("\nWrite action (buy, fill, take, remaining, exit):\n")
            if action == 'buy':
                coffeeMachine.coffee_choice(espresso, latte, cappucino, resources)
            elif action == 'fill':
                coffeeMachine.fill(resources)
            elif action == 'take':
                print (f'I gave you ${resources.money}')
                resources.money = 0
            elif action == 'remaining':
                coffeeMachine.print_remaining()
            else:
                quit()

resources = coffeeMachine(400, 540, 120, 9, 550)
espresso = coffeeMachine(250, 0, 16, 1, 4)
latte = coffeeMachine(350, 75, 20, 1, 7)
cappucino = coffeeMachine(200, 100, 12, 1, 6)

coffeeMachine.choose_your_action()
