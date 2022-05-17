const input = require('prompt-sync')();

console.log(`Welcome to Currency Converter!
1 USD equals  1 USD
1 USD equals  113.5 JPY
1 USD equals  0.89 EUR
1 USD equals  74.36 RUB
1 USD equals  0.75 GBP`)

currency = {
    USD: 1,
    JPY: 113.5,
    EUR: 0.89,
    RUB: 74.36,
    GBP: 0.75,
}

function CurrencyConverter () {
    let from = input('From: ').toUpperCase();
    if (currency[from] === undefined) {
        return "Unknown currency"
    }
    let to = input('To: ').toUpperCase();
    if (currency[to] === undefined) {
        return "Unknown currency"
    }
    let amount = input('Amount: ');
    result = currency[to] * Number(amount) / currency[from]
    if (amount < 0) {
        return "The amount can not be less than 1"}
    else if (isNaN(result)) {
        return "The amount has to be a number"}
    else {
        return `Result: ${amount} ${from} equals ${result.toFixed(4)} ${to}`;
    }    
}

function main () {
    while (true) {
        let choice = input('What do you want to do?\n1-Convert currencies 2-Exit program\n').toUpperCase();
        if (choice == 1) {
            while (true) {
                console.log("What do you want to convert?")
                result = CurrencyConverter()
                if (result != "Unknown currency") {
                    console.log(result);
                    break;
                    }
                console.log(result);
                }
        }
        else if (choice == 2) {
            console.log("Have a nice day!");
            break;
        }
        else {
            console.log("Unknown input");
        }
    }
}


main();
