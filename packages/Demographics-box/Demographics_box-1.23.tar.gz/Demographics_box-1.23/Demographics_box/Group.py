from People import People

class Group:

    """ Class to generate a group of people, with their demographic data. Uses the People class
    """
    
    def __init__(self, n):
        """ Initialization function
            
            args: 
                n: int defining the number of people to create
            
            return: 
                a list of people
        
        """
        self.people = [People() for count in range(n)]
        self.size = n
        
    def __str__(self):
        output = ""
        for count in range(self.size):
            output += str(self.people[count]) + "\n"
        return output
  