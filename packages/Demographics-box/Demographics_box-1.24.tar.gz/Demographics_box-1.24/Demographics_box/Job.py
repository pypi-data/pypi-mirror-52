import random

#age above which the person should be retired
retirement_age = 65

#age below which the person is a kid or student
job_entry = 23

def generate_job(age):
    """Function to return a type of profession

        Args: 
            age: int representing the age of the person

        Returns
            String with a job
    """    
    if(age<job_entry):
        return "kid or student"
    elif(age>retirement_age):
        return "retired"
    else: 
        return random.choice(List_of_jobs)


# List of 50 top jobs in the US  - based on https://www.ranker.com/list/most-common-jobs-in-america/american-jobs
List_of_jobs = [
    "Retail salesperson",
    "Cashier",
    "Office clerk",
    "Combined food preparation and serving worker",
    "Registered nurse",
    "Waiter or waitress",
    "Customer service representative",
    "Janitor or cleaner",
    "Freight, stock, and hand material mover laborer",
    "Secretary or administrative assistant",
    "Stock clerk and order filler",
    "General and operation manager",
    "Bookkeeping, accounting, and auditing clerk",
    "Elementary school teacher",
    "Heavy and tractor-trailer truck driver",
    "Nursing aide, orderlies, and attendant",
    "Wholesale and manufacturing sales representative",
    "First-line supervisor of office and administrative support workers",
    "Teacher assistant",
    "Bus and truck mechanics and diesel engine specialist",
    "Maintenance and repair worker",
    "First-line supervisor of retail sales workers",
    "Executive secretary and executive administrative assistant",
    "Accountant and auditor",
    "Secondary school teacher",
    "Security guard",
    "Receptionist and information clerk",
    "Business operations specialist",
    "Home health aide",
    "Team assembler",
    "Restaurant Cook",
    "Maid and housekeeping cleaner",
    "Landscaping and groundskeeping worker",
    "Food preparation worker",
    "Light truck or delivery service driver",
    "Construction laborer",
    "First-line supervisor of food preparation and serving workers",
    "Licensed practical and licensed vocational nurse",
    "Shipping, receiving, and traffic clerk",
    "Personal care aide",
    "Packer and packager",
    "Middle school teacher",
    "Police and sheriff's patrol officer",
    "Carpenter",
    "Childcare worker",
    "Automotive service technicians and mechanic",
    "Computer support specialist",
    "Lawyer",
    "Teller",
    "First-line supervisor of production and operating worker",
    "Management analyst",
    "Service Sales representative",
    "Fast food Cook"]