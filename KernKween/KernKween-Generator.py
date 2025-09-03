#MenuTitle: KernKween
# -*- coding: utf-8 -*-
#Based on the wordlist KernKing
from __future__ import division, print_function, unicode_literals
__doc__="""
KernKween- Select between lowercase and uppercase kerning word lists
and get a user-specified number of random words from the selected list.
"""

import GlyphsApp
import random
import vanilla

class KernKween(object):
    def __init__(self):
        # Word lists
        self.lc_lc = """
lynx tuft frogs, dolphins abduct by proxy the ever awkward klutz, dud, dummkopf, jinx snubnose filmgoer, orphan sgt. renfruw grudgek reyfus, md. sikh psych if halt tympany jewelry sri heh! twyer vs jojo pneu fylfot alcaaba son of nonplussed halfbreed bubbly playboy guggenheim daddy coccyx sgraffito effect, vacuum dirndle impossible attempt to disvalue, muzzle the afghan czech czar and exninja, bob bixby dvorak wood dhurrie savvy, dizzy eye aeon circumcision uvula scrungy picnic luxurious special type carbohydrate ovoid adzuki kumquat bomb? afterglows gold girl pygmy gnome lb. ankhs acme aggroupment akmed brouhha tv wt. ujjain ms. oz abacus mnemonics bhikku khaki bwana aorta embolism vivid owls often kvetch otherwise, wysiwyg densfort wright you/quoteright ve absorbed rhythm, put obstacle kyaks krieg kern wurst subject enmity equity coquet quorum pique tzetse hepzibah sulfhydryl briefcase ajax ehler kafka fjord elfship halfdressed jugful eggcup hummingbirds swingdevil bagpipe legwork reproachful hunchback archknave baghdad wejh rijswijk rajbansi rajput ajdir okay weekday obfuscate subpoena liebknecht marcgravia ecbolic arcticward dickcissel pincpinc boldface maidkin adjective adcraft adman dwarfness applejack darkbrown kiln palzy always farmland flimflam unbossy nonlineal stepbrother lapdog stopgap sx countdown basketball beaujolais vb. flowchart aztec lazy bozo syrup tarzan annoying dyke yucky hawg gagzhukz cuzco squire when hiho mayhem nietzsche szasz gumdrop milk emplotment ambidextrously lacquer byway ecclesiastes stubchen hobgoblins crabmill aqua hawaii blvd. subquality byzantine empire debt obvious cervantes jekabzeel anecdote flicflac mechanicville bedbug couldn/quoteright t i/quoteright ve it/quoteright s they/quoteright ll they/quoteright d dpt. headquarter burkhardt xerxes atkins govt. ebenezer lg. lhama amtrak amway fixity axmen quumbabda upjohn hrumpf
"""
        
        self.UC_lc = """
Aaron Abraham Adam Aeneas Agfa Ahoy Aileen Akbar Alanon Americanism Anglican Aorta April Fool/quoteright s Day Aqua Lung (Tm.) Arabic Ash Wednesday Authorized Version Ave Maria Away Axel Ay Aztec Bhutan Bill Bjorn Bk Btu. Bvart Bzonga California Cb Cd Cervantes Chicago Clute City, Tx. Cmdr. Cnossus Coco Cracker State, Georgia Cs Ct. Cwacker Cyrano David Debra Dharma Diane Djakarta Dm Dnepr Doris Dudley Dwayne Dylan Dzerzhinsk Eames Ectomorph Eden Eerie Effingham, Il. Egypt Eiffel Tower Eject Ekland Elmore Entreaty Eolian Epstein Equine Erasmus Eskimo Ethiopia Europe Eva Ewan Exodus Jan van Eyck Ezra Fabian February Fhara Fifi Fjord Florida Fm France Fs Ft. Fury Fyn Gabriel Gc Gdynia Gehrig Ghana Gilligan Karl Gjellerup Gk. Glen Gm Gnosis Gp.E. Gregory Gs Gt. Br. Guinevere Gwathmey Gypsy Gzags Hebrew Hf Hg Hileah Horace Hrdlicka Hsia Hts. Hubert Hwang Hai Hyacinth Hz. Iaccoca Ibsen Iceland Idaho If Iggy Ihre Ijit Ike Iliad Immediate Innocent Ione Ipswitch Iquarus Ireland Island It Iud Ivert Iwerks Ixnay Iy Jasper Jenks Jherry Jill Jm Jn Jorge Jr. Julie Kerry Kharma Kiki Klear Koko Kruse Kusack Kylie Laboe Lb. Leslie Lhihane Llama Lorrie Lt. Lucy Lyle Madeira Mechanic Mg. Minnie Morrie Mr. Ms. Mt. Music My Nanny Nellie Nillie Novocane Null Nyack Oak Oblique Occarina Odd Oedipus Off Ogmane Ohio Oil Oj Oklahoma Olio Omni Only Oops Opera Oqu Order Ostra Ottmar Out Ovum Ow Ox Oyster Oz Parade Pd. Pepe Pfister Pg. Phil Pippi Pj Please Pneumonia Porridge Price Psalm Pt. Purple Pv Pw Pyre Qt. Quincy Radio Rd. Red Rhea Right Rj Roche Rr Rs Rt. Rural Rwanda Ryder Sacrifice Series Sgraffito Shirt Sister Skeet Slow Smore Snoop Soon Special Squire Sr St. Suzy Svelte Swiss Sy Szach Td Teach There Title Total Trust Tsena Tulip Twice Tyler Tzean Ua Udder Ue Uf Ugh Uh Ui Uk Ul Um Unkempt Uo Up Uq Ursula Use Utmost Uvula Uw Uxurious Uz/germandbls ai Valerie Velour Vh Vicky Volvo Vs Water Were Where With World Wt. Wulk Wyler Xavier Xerox Xi Xylophone Yaboe Year Yipes Yo Ypsilant Ys Yu Zabar/quoteright s Zero Zhane Zizi Zorro Zu Zy Don/quoteright t I/quoteright ll I/quoteright m I/quoteright se
"""
        
        # Create the window
        self.w = vanilla.Window((350, 180), "KernKween")
        
        # Selection group
        self.w.selectionGroup = vanilla.Group((20, 20, -20, 100))
        self.w.selectionGroup.titleText = vanilla.TextBox((5, 0, -10, 20), "Select Word List:")
        self.w.selectionGroup.lowercaseRadio = vanilla.RadioButton((5, 20, 100, 25), "lc - lc", value=True, callback=self.radioCallback)
        self.w.selectionGroup.uppercaseRadio = vanilla.RadioButton((110, 20, 100, 25), "Uc - lc", callback=self.radioCallback)
        
        # Number of words input
        self.w.numWordsLabel = vanilla.TextBox((20, 80, 120, 20), "Number of words:")
        self.w.numWordsInput = vanilla.EditText((140, 80, 40, 20), "20")
        
        # Close button
        self.w.closeButton = vanilla.Button((20, 120, 120, 25), "Close", callback=self.closeWindow)
        
        # Generate button
        self.w.generateButton = vanilla.Button((-140, 120, 120, 25), "Generate", callback=self.generateWords)
        
        # Status indicator
        self.w.statusText = vanilla.TextBox((20, 150, -20, 25), "❌ Nothing there yet")
        
        # Open window
        self.w.open()
    
    def radioCallback(self, sender):
        """Handle radio button selection"""
        if sender == self.w.selectionGroup.lowercaseRadio:
            self.w.selectionGroup.uppercaseRadio.set(False)
        else:
            self.w.selectionGroup.lowercaseRadio.set(False)
    
    def closeWindow(self, sender):
        """Close the window"""
        self.w.close()
    
    def generateWords(self, sender):
        # Get selected word list
        if self.w.selectionGroup.lowercaseRadio.get():
            word_list = self.lc_lc
            selection_type = "Lowercase"
        else:
            word_list = self.UC_lc
            selection_type = "Uppercase"
        
        # Parse words (split by whitespace and filter out empty strings)
        words = [word.strip() for word in word_list.split() if word.strip()]
        
        # Get number of words from input
        try:
            num_words = int(self.w.numWordsInput.get())
            if num_words < 1:
                raise ValueError
        except Exception:
            self.w.statusText.set("❌ Enter a valid number")
            return
        
        # Generate random words
        if len(words) >= num_words:
            selected_words = random.sample(words, num_words)
        else:
            selected_words = words  # If less than requested, use all
        
        # Create text for current tab
        tab_text = " ".join(selected_words)
        
        # Use current tab in Glyphs
        try:
            Font = Glyphs.font
            if Font:
                currentTab = Font.currentTab
                if currentTab:
                    currentTab.text = tab_text
                    self.w.statusText.set("✔️ Yes Babe")
                else:
                    Font.newTab(tab_text)
                    self.w.statusText.set("✔️ Yes Babe")
            else:
                self.w.statusText.set("❌")
        except Exception as e:
            self.w.statusText.set("❌")

# Run the GUI
KernKween() 