import random

#definition of the max age of one person
max_age = 80

class People: 
    """ Generic class for generating demographic data. At the moment, starts with very basic demographic info: 
            - First name 
            - Last name
            - Age
            - State of residence
            - Job
    """
    
    def __init__(self): 
        """ creates new person, using the modules and list of sample data in the folder Modules """ 
        
        #randomly decides if person is male or female (for first name generator)
        is_female = random.getrandbits(1)
        
        self.first_name = First_name.generate_first_name(is_female)
        #self.last_name = Modules.generate_last_name()   
        #self.us_state = Modules.generate_us_state()
        #self.age = Modules.generate_age(max_age)
        #self.job = Modules.generate_job(self.age)
        
    def __str__(self):
        return "{} {}, {}, {}, {}".format(self.first_name, self.last_name, self.age, self.us_state, self.job)
        