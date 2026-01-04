import datetime
import os
import json

materials = {
    1: "Plastic",
    2: "Paper",
    3: "Metal",
    4: "Oil",
    5: "Main menu"
}

materialPrice = {
    "Plastic": 0.3,
    "Paper": 0.5,
    "Metal": 0.8,
    "Oil": 5
}

if os.path.exists("material_price.json"):
    try:
        with open("material_price.json", "r") as f:
            materialPrice = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning, some issue happened")

savings = {
    "Plastic": 0,
    "Paper": 0,
    "Metal": 0,
    "Oil": 0,
    "Total": 0
}

recycleHistory = {
    "Plastic": [],
    "Paper": [],
    "Metal": [],
    "Oil": []
}

HISTORY_FILE = "recycling_history.json"

def loadHistory():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                loadedHistory = json.load(f)
                for material in recycleHistory:
                    if material in loadedHistory:
                        recycleHistory[material] = loadedHistory[material]
                recalculateSavings()
        except (json.JSONDecodeError, IOError):
            print("Warning.")

def recalculateSavings():
    for material in savings:
        savings[material] = 0
    
    for material in recycleHistory:
        for entry in recycleHistory[material]:
            amount = entry[1]
            savings[material] += amount
            savings["Total"] += amount * materialPrice[material]

def saveHistory():
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(recycleHistory, f)
    except IOError:
        print("Warning.")

def save(material, amount):
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    recycleHistory[material].append((date, amount))
    saveHistory()
    
def saveSavings():
    try:
        with open("savings.json", "w") as f:
            json.dump(savings, f)
    except IOError:
        print("Warning: Could not save savings data.")

def loadSavings():
    if os.path.exists("savings.json"):
        try:
            with open("savings.json", "r") as f:
                loadedSavings = json.load(f)
                for material in savings:
                    if material in loadedSavings:
                        savings[material] = loadedSavings[material]
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not load savings data.")


def main():
    loadHistory()
    loadSavings()
    while True:
        print("\n--- Recycle ---")
        print("1- Insert material type -> ")
        print("2- Change recycle price for each material ->")
        print("3- Total savings ->")
        print("4- Recycling history -> ")
        print("5- Spend savings ->")
        print("6- Exit\n")

        choice = int(input("Please enter your choice: "))
        
        if choice==1:
            insertMaterial()
        elif choice==2:
            changePrice()
        elif choice==3:
            totalSavings()
        elif choice==4:
            recyclingHistory()
        elif choice ==5:
            spendSavings()
        elif choice==6:
            print("Program has terminated.")
            break
        else: 
            print("---Enter valid number---\n")

def insertMaterial():
    while True:
        print("\nAvailable materials:")
        for num, material in materials.items():
            print(f"{num}: {material}")
        
        try:
            choice = int(input("\nSelect the material/or exit (5): "))
        except ValueError:
            print("Please enter a valid number")
            continue
            
        if choice == 5:
            break
        elif choice in materials:
            material = materials[choice]
            try:
                amount = float(input(f"{material} amount(piece/liter): "))
                if amount <= 0:
                    print("Invalid, amount must be positive")
                    continue
                
                save(material, amount)
                
                savings[material] += amount
                earning = amount * materialPrice[material]
                savings["Total"] += earning
                
                print(f"\nAdded {amount} of {material}. Earned ${earning:.2f}")
                print("---Saved in the log---\n")
            except ValueError:
                print("Please enter a valid number for amount")
        else:
            print("Invalid material selection")
            

def changePrice():
    admin00 ="1234"
    while True:
        adminP = input("Please enter admin password (or type 'exit' to cancel): ")

        if adminP.lower() == "exit":
            print("Password entry cancelled.")
            return

        if adminP == admin00:
            print("\n--- Price Update Center ---")
            for material in materialPrice:
                try:
                    newPrice = float(input(f"{material} (Current Price: {materialPrice[material]}): "))
                    if newPrice >= 0:
                        materialPrice[material] = newPrice
                    else:
                        print("Invalid entry, price must be non-negative.")
                except ValueError:
                    print("Please enter a valid number.")

            with open("material_price.json", "w") as f:
                json.dump(materialPrice, f)

            print("\n--- Prices saved successfully ---\n")
            break  # exits the password loop after success
        else:
            print("Wrong password. Try again.\n")
        
def totalSavings():
    print("\n---Total Savings---")
    for material in savings:
        print(material, savings[material])
    

def recyclingHistory():
    print("\n---Recycling History---")
    for material, entries in recycleHistory.items():
        print(f"\n{material} recycling history:")
        if not entries:
            print("  No entries yet")
            continue
        for entry in entries:
            date, amount = entry
            print(f"  Date: {date}, Amount: {amount}, Value: ${amount * materialPrice[material]:.2f}")
    print(f"\nTotal savings: ${savings['Total']:.2f}")

def spendSavings():
    print("\n--- Spend Savings ---")
    print("Current savings:")
    
    for material, amount in savings.items():
        if material == "Total":
            continue        
        else:
            print(f"{material}: {amount} units")
            
    entry= input("\nEnter the material name:").strip().capitalize()
            
    if entry == "Plastic":
        try:
            plastic = float(input("\nEnter the amount you want to spend: "))
            if plastic <= 0 or plastic > savings["Plastic"]:
                print("amount can't be out of the range")
            else:
                savings["Plastic"] -= plastic
                savings["Total"] -= plastic * materialPrice["Plastic"]
                saveSavings()
                print("\n---progress is completed succesfully---")
        except ValueError:
            print("Please enter a valid number")
            
    elif entry == "Paper":
        try:
            paper = float(input("\nEnter the amount you want to spend: "))
            if paper <= 0 or paper > savings["Paper"]:
                print("amount can't be out of the range")
            else:
                savings["Paper"] -= paper
                savings["Total"] -= paper * materialPrice["Paper"]  
                saveSavings()
                print("\n---progress is completed succesfully---")
        except ValueError:
            print("Please enter a valid number")
            
    elif entry == "Metal":
        try:
            metal =float(input("\nEnter the amount you want to spend: "))
            if metal <= 0 or metal > savings["Metal"]:
                print("amount can't be out of the range")
            else:
                savings["Metal"] -= metal
                savings["Total"] -= metal * materialPrice["Metal"]
                saveSavings()
                print("\n---progress is completed succesfully---")
        except ValueError:
            print("Please enter a valid number")
            
    elif entry == "Oil":
        try:
            oil = float(input("\nEnter the amount you want to spend: "))
            if oil <= 0 or oil > savings["Oil"]:
                print("amount can't be out of the range")
            else:
                savings["Oil"] -= oil
                savings["Total"] -= oil * materialPrice["Oil"]
                saveSavings()
                print("\n---progress is completed succesfully---")
        except ValueError:
            print("Please enter a valid number")
    else:
        print("invalid entry, Please enter from Plastic,Paper,Metal,Oil")
                
        
main()
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    