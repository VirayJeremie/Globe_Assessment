import random

class Credentials():
    def __init__(self):
        random_gen_num = random.randrange(0,1000000)
        self.user_username = str(random_gen_num)+"@hotmail.com"
        self.user_password = "manggo_123"
        
