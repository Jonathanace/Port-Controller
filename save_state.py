import pickle
import string

# take the type of operation, 
# operation steps (balancing, loading/unloading), 
# current step of operation, 
# manifest file name 
# and store into file
# example: displaying balancing step 5 and after moving onto step 6, save_state("balancing", solution_steps, 5, "ShipCase1.txt") 
def save_state(operation: string, objects, curr_step: int, manifest: string): 
    try:
        with open("state.pkl", 'wb') as file:
            pickle.dump([objects, curr_step, manifest], file)
    except:
        print("Could not save state into file")

# check if a saved state file exists
#  and returns the saved state in a list containing type of operation, operation steps, current step of operation, and manifest file. 
# If not prints an error.
def get_state():
    try:
        with open('state.pkl', 'rb') as file:
            restored_state = pickle.load(file)
            return restored_state
    except FileNotFoundError:
        print("Error: state.pkl not found")
    except pickle.UnpicklingError:
        print("Error: state.pkl could not be unpickled")
        