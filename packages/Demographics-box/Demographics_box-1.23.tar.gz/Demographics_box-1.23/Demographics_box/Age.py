import random

def generate_age(max_age):
    """Function to return an age.
    
        Args: 
            max_age: int representing the max age possible
    
        returns
            int: a random value for the possible age
    """
    return random.randint(1,max_age)