#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions to create an inventory of CD Titles and Artists.
# Change Log: (Who, When, What)
# MPoehler, 2021-Feb-17, Retrived file created by DBiesinger
# MPoehler, 2021-Feb-19, Modified script, replaced TODOs with appropriate code
# MPoehler, 2021-Feb-19, Added Doc String to recently added functions
# MPoehler, 2021-Feb-26, Changed data store from text to binary and Error Handling for empty or nonexistent file.
# MPoehler. 2021-Feb-27, Added Error Handling for ValueError to keep program running if a letter is entered in a numbers place.
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dicRow = {}  # dict of data row
strFileName = 'CDInventory.bin'  # data storage file
objFile = None  # file object
import pickle


# -- PROCESSING -- #

class DataProcessor:
    """Handling of data in memory during runtime"""

    @staticmethod
    def add_Inv(data_list):
        """Function to add user data into 2D list of dictionaries as inventory management

        Args:
            datalist (return value of get_data() function): contains the user input as a list

        Resturns:
            dicRow (dict): user data in a dictionary
            lstTbl (2D list of dict): append 2D list of dicts with recent user data
        """
        intID = int(data_list[0])
        dicRow = {'ID': intID, 'CD Title': data_list[1], 'Artist': data_list[2]}
        lstTbl.append(dicRow)
        return lstTbl

    @staticmethod
    def del_Inv(user_input):
        """Function to delete specifc data from list depending on user choice
        
        Args:
            user_input (int): integer data stored in a variable created in 3.5.1.2 (Section of main loop that handles data deletion)
            
        Returns:
            Updated lstTbl with specfic entry removed or a statement stating that entry entered does not exist
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == user_input:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        return blnCDRemoved


class FileProcessor:
    """Handling of data in and out of a binary file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from binary file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as objFile:
            table = pickle.load(objFile)
        return table

    def update_file(file_name, table):
        """Function that overwrites binary file with updated inventory data
        
        Args:
            file_name (string): name of file used to write data back into
            table (list of dicts): 2D data structure (list of dicts) that holds invenotry data during runtime
            
        Returns:
            None
        """
        with open(file_name, 'wb') as objFile: # this opens the data file to overwrite with data currently in the inventory
            pickle.dump(table, objFile)
        objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('\nMenu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('\n======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def get_data():
        """Captures the user data for inventory
        
        Args:
            None
            
        Returns:
            strID (string): ID data string to be converted to int
            StrTitle (string): CD Title data string
            strArtis (string): Artist data string
            
        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return [strID, strTitle, strArtist]

# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName, lstTbl)
except FileNotFoundError:
    print('\nFile:', strFileName, ', Does not exist. Please save Inventory data to create file.')
except EOFError:
    print('\nFile is empty. Please save CD Inventory data.')


# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...\n')
            lstTbl = FileProcessor.read_file(strFileName, lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.\n')
            # IO.show_inventory(lstTbl)
        # We can move this outside the if block and then only need the one line of code.
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        try:
        # 3.3.1 Ask user for new ID, CD Title and Artist
            datLst = IO.get_data()
        # 3.3.2 Add item to the table
            DataProcessor.add_Inv(datLst)
        except ValueError:
            print('\nEntry Error!')
            print('If you would like to add an entry please enter an integer(number) for an ID.')
        finally:
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        try:
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
            # 3.5.1.2 ask user which ID to remove
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            cd_removed = DataProcessor.del_Inv(intIDDel)
            if cd_removed:
                print('\nThe CD was removed\n')
            else:
                print('\nCould not find this CD!\n')
            IO.show_inventory(lstTbl)
        except ValueError:
                print('\nEntry Error!')
                print('Please enter the integer(number) for the ID you want to delete')
        continue

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.update_file(strFileName, lstTbl)
            print('Inventory file has been updated\n')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')