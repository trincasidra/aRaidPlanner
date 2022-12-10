import pickle, os.path, tkinter as tk
from tkinter import messagebox, ttk

characters_filepath = "characters.pkl"
encounters_filepath = "encounters.pkl"
characters = {}
encounters = {}

classes = [
    "Warrior",
    "Paladin",
    "Hunter",
    "Rogue",
    "Priest",
    "Death Knight",
    "Shaman",
    "Mage",
    "Warlock",
    "Monk",
    "Druid",
    "Demon Hunter",
    "Evoker"
]

specs = [
    ["Arms", "Fury", "Protection"],
    ["Holy", "Protection", "Retribution"],
    ["Beast Mastery", "Marksmanship", "Survival"],
    ["Assassination", "Outlaw", "Subtlety"],
    ["Discipline", "Holy", "Shadow"],
    ["Blood", "Frost", "Unholy"],
    ["Elemental", "Enhancement", "Restoration"],
    ["Arcane", "Fire", "Frost"],
    ["Affliction", "Demonology", "Destruction"],
    ["Brewmaster", "Windwalker", "Mistweaver"],
    ["Balance", "Feral", "Guardian", "Restoration"],
    ["Havoc", "Vengeance"],
    ["Devastation", "Preservation"]
]

cooldowns = {
    "WarriorArms": [],
    "WarriorFury": [],
    "WarriorProtection": [],
    "PaladinHoly": [],
    "PaladinProtection": [],
    "PaladinRetribution": [],
    "HunterBeast Mastery": [],
    "HunterMarksmanship": [],
    "HunterSurvival": [],
    "RogueAssassination": [],
    "RogueOutlaw": [],
    "RogueSubtlety": [],
    "PriestDiscipline": [],
    "PriestHoly": [],
    "PriestShadow": [],
    "Death KnightBlood": [],
    "Death KnightFrost": [],
    "Death KnightUnholy": [],
    "ShamanElemental": [],
    "ShamanEnhancement": [],
    "ShamanRestoration": [],
    "MageArcane": [],
    "MageFire": [],
    "MageFrost": [],
    "WarlockAffliction": [],
    "WarlockDemonology": [],
    "WarlockDestruction": [],
    "MonkBrewmaster": [],
    "MonkWindwalker": [],
    "MonkMistweaver": [],
    "DruidBalance": [],
    "DruidFeral": [],
    "DruidGuardian": [],
    "DruidRestoration": [],
    "Demon HunterHavoc": [],
    "Demon HunterVengeance": [],
    "EvokerDevastation": [],
    "EvokerPreservation": []
}

bosses = [
    "Eranog",
    "Terros",
    "The Primalist Council",
    "Sennarth, The Cold Breath",
    "Dathea, Ascended",
    "Kurog Grimtotem",
    "Broodkeeper Diurna",
    "Raszageth the Storm-Eater"
]

class PlannerGUI:
    def __init__(self):
        global characters
        global encounters

        if os.path.exists(characters_filepath):
            with open (characters_filepath, "rb") as f:
                characters = pickle.load(f)

        if os.path.exists(encounters_filepath):
            with open (encounters_filepath, "rb") as f:
                encounters = pickle.load(f)
        else:
            for boss in bosses:
                for x in range(0, 8):
                    encounters[boss+str(x)] = {}
            with open (encounters_filepath, "wb") as f:
                pickle.dump(encounters, f)

        self.root = tk.Tk()

        self.root.geometry("1024x800")
        self.root.title("aRaidPlanner")

        self.raid_planner_label = tk.Label(self.root, text="Raid Planner", font=('Arial', 18))
        self.raid_planner_label.pack(padx=20, pady=20)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.columnconfigure(2, weight=1)
        self.main_frame.columnconfigure(3, weight=1)

        self.characters_button = tk.Button(self.main_frame, text="Characters", font=('Arial', 18), height=8, command=self.show_characters)
        self.characters_button.grid(row=0, column=1, sticky=tk.W+tk.E, padx=30)

        self.encounters_button = tk.Button(self.main_frame, text="Encounters", font=('Arial', 18), height=8, command=self.show_encounters)
        self.encounters_button.grid(row=0, column=2, sticky=tk.W+tk.E, padx=30)

        self.main_frame.pack(fill="x")

        self.root.mainloop()

    def class_picked(self, event):
        self.character_spec_picker["stat"] = "readonly"
        self.character_class = self.character_class_picker.get()
        index = classes.index(self.character_class)
        self.character_spec_picker.config(values=specs[index])
        self.character_spec = ''
        self.character_spec_picker.set(self.character_spec)
        self.disable_save_character()

    def spec_picked(self, event):
        self.character_spec = self.character_spec_picker.get()
        self.disable_save_character()

    def name_inputted(self, event):
        self.disable_save_character()

    def save_character(self):
        characters[self.character_name_entry.get()] = self.character_class+'.'+self.character_spec
        with open (characters_filepath, "wb") as f:
            pickle.dump(characters, f)
        self.show_characters()

    def delete_character(self, character_name):
        print(self, character_name)
        characters.pop(character_name)
        with open (characters_filepath, "wb") as f:
            pickle.dump(characters, f)
        self.show_characters()

    def disable_save_character(self):
        if self.character_class == '' or self.character_spec == '' or self.character_name_entry.get() == '':
            self.save_button["state"] = "disabled"
        else:
            self.save_button["state"] = "normal"

    def show_main(self):
        pass

    def show_characters(self):
        self.destroy_widgets()

        self.character_frame = tk.Frame(self.root)

        self.character_name = tk.StringVar()
        self.character_class = tk.StringVar()
        self.character_spec = tk.StringVar()

        self.character_frame_label = tk.Label(self.character_frame, text="Character Manager", font=('Arial', 18))
        self.character_frame_label.pack(padx=20, pady=20)

        self.character_class_picker = ttk.Combobox(self.character_frame, width=10, value=(classes), state="readonly")
        self.character_class_picker.pack()
        self.character_class_picker.bind('<<ComboboxSelected>>', self.class_picked)

        self.character_spec_picker = ttk.Combobox(self.character_frame, width=10, state="disabled")
        self.character_spec_picker.pack()
        self.character_spec_picker.bind('<<ComboboxSelected>>', self.spec_picked)

        self.character_name_entry = tk.Entry(self.character_frame, font=('Arial, 16'))
        self.character_name_entry.pack()
        self.character_name_entry.bind('<Key>', self.name_inputted)

        self.save_button = tk.Button(self.character_frame, text="Save", font=('Arial', 14), command=self.save_character, state="disabled")
        self.save_button.pack(padx=10, pady=10)

        self.character_table = tk.Frame(self.character_frame)
        self.character_table.columnconfigure(0, weight=1)
        self.character_table.columnconfigure(1, weight=1)
        self.character_table.columnconfigure(2, weight=1)
        self.character_table.columnconfigure(3, weight=1)
        self.character_table.columnconfigure(4, weight=1)

        index = 0
        for character_name, character_class_spec in characters.items():
            self.character_table.rowconfigure(index, weight=1, minsize=45)
            name_cell = tk.Frame(master=self.character_table, relief=tk.RIDGE, borderwidth=1.5)
            name_cell.grid(row=index, column=1, sticky=tk.W+tk.E, pady=3)
            name_cell_text = tk.Label(master=name_cell, text=character_name)
            name_cell_text.pack()
            character_data = character_class_spec.split('.')
            class_cell = tk.Frame(master=self.character_table, relief=tk.RIDGE, borderwidth=1.5)
            class_cell.grid(row=index, column=2, sticky=tk.W+tk.E, pady=3)
            class_cell_text = tk.Label(master=class_cell, text=character_data[0])
            class_cell_text.pack()
            spec_cell = tk.Frame(master=self.character_table, relief=tk.RIDGE, borderwidth=1.5)
            spec_cell.grid(row=index, column=3, sticky=tk.W+tk.E, pady=3)
            spec_cell_text = tk.Label(master=spec_cell, text=character_data[1])
            spec_cell_text.pack()
            delete_cell = tk.Frame(master=self.character_table, relief=tk.RIDGE, borderwidth=1.5)
            delete_cell.grid(row=index, column=4, sticky=tk.W, pady=3)
            delete_cell_button = tk.Button(delete_cell, text="Delete", font=('Arial', 12), command=lambda character_name=character_name: self.delete_character(character_name))
            delete_cell_button.pack()
            index += 1

        self.character_table.pack(fill="x")

        self.show_encounters_button = tk.Button(self.character_frame, text="Encounters", font=('Arial', 14), command=self.show_encounters)
        self.show_encounters_button.place(anchor="ne", rely=0.0, relx=1.0, x=-10, y=10)

        self.character_frame.pack(fill="x")


    def show_encounters(self):
        self.destroy_widgets()

        self.encounters_frame = tk.Frame(self.root)

        self.encounters_frame_label = tk.Label(self.encounters_frame, text="Encounters Manager", font=('Arial', 18))
        self.encounters_frame_label.pack(padx=20, pady=20)

        self.encounters_table = tk.Frame(self.encounters_frame)
        self.encounters_table.columnconfigure(0, weight=1)
        self.encounters_table.columnconfigure(1, weight=3)
        self.encounters_table.columnconfigure(2, weight=1)
        self.encounters_table.columnconfigure(3, weight=1)
        self.encounters_table.columnconfigure(4, weight=1)
        self.encounters_table.columnconfigure(5, weight=1)
        self.encounters_table.columnconfigure(6, weight=1)
        self.encounters_table.columnconfigure(7, weight=1)
        self.encounters_table.columnconfigure(8, weight=1)
        self.encounters_table.columnconfigure(9, weight=1)
        self.encounters_table.columnconfigure(10, weight=1)
        self.encounters_table.columnconfigure(11, weight=1)

        index = 0
        for boss in bosses:
            self.encounters_table.rowconfigure(index, weight=1, minsize=45)
            name_cell = tk.Frame(master=self.encounters_table, relief=tk.RIDGE, borderwidth=1.5)
            name_cell.grid(row=index, column=1, sticky=tk.W+tk.E, pady=3)
            name_cell_text = tk.Label(master=name_cell, text=boss)
            name_cell_text.pack()
            for x in range(0, 8):
                encounter_cell = tk.Frame(master=self.encounters_table, relief=tk.RIDGE, borderwidth=1.5)
                encounter_cell.grid(row=index, column=x+2, sticky=tk.W+tk.E, pady=3)
                new_ecounter_button = tk.Button(encounter_cell, text=x+1, font=('Arial', 12), command=lambda boss=boss, slot=x: self.manage_encounter(boss, slot))
                new_ecounter_button.pack()
            index += 1

        self.encounters_table.pack(fill="x")

        self.show_characters_button = tk.Button(self.encounters_frame, text="Characters", font=('Arial', 14), command=self.show_characters)
        self.show_characters_button.place(anchor="ne", rely=0.0, relx=1.0, x=-10, y=10)

        self.encounters_frame.pack(fill="x")

    def manage_encounter(self, boss, slot):
        print(boss+'.'+str(slot))

    def destroy_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

PlannerGUI()
