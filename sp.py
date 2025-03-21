

class SP():
    def __init__(self, 
                 max_distance, 
                 sp_set):
        self.max_distance = max_distance
        self.sp_set = sp_set
        self.sp_status = [0 for _ in range(len(sp_set))]
        
    def is_avaliable(self, berth_loaction):
        for idx, sp in enumerate(self.sp_set):
            if not self.sp_status[idx] and self.get_distance(sp, berth_loaction) <= self.max_distance:
                self.sp_status[idx] = 1
                return True
        return False
    
    def get_distance(self, sp, berth_loaction):
        return abs(sp - berth_loaction)