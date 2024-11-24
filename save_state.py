import pickle

# take the operation steps (balancing, loading/unloading) and the current step of operation and store into pickle file
# example: displaying balancing step 5 and after moving onto step 6, save_state(solution_steps, 5) 
def save_state(objects, curr_step: int): 
    try:
        with open("state.pkl", 'wb') as file:
            pickle.dump([objects, curr_step], file)
    except:
        print("Could not save state into file")

# check if a saved state file exists, and returns the saved state. If not prints an error.
def get_state():
    try:
        with open('state.pkl', 'rb') as file:
            restored_state = pickle.load(file)
            return restored_state
    except FileNotFoundError:
        print("Error: state.pkl not found")
    except pickle.UnpicklingError:
        print("Error: state.pkl could not be unpickled")
        