import pickle

def save_state(objects, curr_step: int): 
    try:
        with open("state.pkl", 'wb') as file:
            pickle.dump([objects, curr_step], file)
    except:
        print("Could not save state into file")


def get_state():
    try:
        with open('state.pkl', 'rb') as file:
            restored_state = pickle.load(file)
            return restored_state
    except FileNotFoundError:
        print("Error: state.pkl not found")
    except pickle.UnpicklingError:
        print("Error: state.pkl could not be unpickled")
        