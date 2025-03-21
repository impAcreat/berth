from ship import Ship
from sp import SP
from data_loader import DataLoader
from model import Model

class BerthArrangement():
    def __init__(self, V, L, E):
        self.V = V
        self.L = L      # shore length
        self.E = E      # shore power(sp) set
    
    
    def get_mn(self, b, s, l, t):
        num_ships = len(b)
        m = [[0] * num_ships for _ in range(num_ships)]
        n = [[0] * num_ships for _ in range(num_ships)]

        for i in range(num_ships):
            for j in range(num_ships):
                if i == j:
                    continue

                # time
                if not (s[i] + t[i] <= s[j] or s[j] + t[j] <= s[i]):
                    m[i][j] = 1
                    
                # space
                if not (b[i] + l[i] <= b[j] or b[j] + l[j] <= b[i]):
                    n[i][j] = 1

        return m, n
    
    
    def get_target_score(self):
        # TODO
        pass
    
    def arrange(self):
        # TODO
        # get decision variables ---------
        b = None
        s = None
        # --------------------------------
        
        
        ## process
        assert len(b) == len(self.V)
        assert len(s) == len(self.V)
        
        rearrange_times = []
        for idx, (berth_location, start_time) in enumerate(zip(b, s)):
            ship = self.V[idx]
            end_time = start_time + ship.process_time
            rearrange_times.append((end_time, idx))
            
            if ship.support_sp and self.E.is_avaliable(berth_location):
                use_sp = True
            else:
                use_sp = False
                
            ship.operate(start_time, end_time, use_sp)
        
        cur_m, cur_n = self.get_mn(b, s, 
                                   [ship.l for ship in self.V],
                                   [ship.process_time for ship in self.V])
        self.efficiency_score, self.emmision_score = self.get_target_score()
        
        
        # TODO: 多条船同时离开
        
        rearrange_times.sort()
        
        ## rearrange
        for time, idx in rearrange_times:
            if self.need_rearrange():
                # update status
                self.V[idx].isfinished = True
                
                self.rearrange(time)

            
    def need_rearrange(self):
        # TODO
        pass
    
    
    def rearrange(self, time):
        # TODO
        # get decision variables ---------
        new_b, new_s = Model().generate()
        new_b = None
        new_s = None
        # --------------------------------
        
        ## process
        assert len(new_b) == len(self.V)
        assert len(new_s) == len(self.V)
        
        rearrange_times = []
        for idx, (berth_location, start_time) in enumerate(zip(new_b, new_s)):
            ship = self.V[idx]
            if ship.isfinished or ship.beth_location == berth_location:
                continue
            
            if len(ship.record) > 0:
                # update info
                last_record = ship.record[-1]
                last_record["end_time"] = time
                last_record["operation_time"] = time - last_record["start_time"]
                ship.record[-1] = last_record
                cur_process_time = ship.process_time - last_record["operation_time"]
                ship.process_time = cur_process_time
            else:
                cur_process_time = ship.process_time
                
            start_time = time + start_time          # TODO
            end_time = start_time + ship.process_time
            rearrange_times.append((end_time, idx))
            
            if ship.support_sp and self.E.is_avaliable(berth_location):
                use_sp = True
            else:
                use_sp = False
                
            ship.operate(start_time, end_time, use_sp)
            
        efficiency_score, emmision_score = self.get_target_score()
        
        return efficiency_score, emmision_score, rearrange_times


if __name__ == "__main__":
    ##
    shore_length = 1000
    d = 50
    
    ##   
    dataloader = DataLoader()  
    ship_set = dataloader.load_ship_data()
    sp_set = dataloader.load_sp_data()
    
    ##
    obj = BerthArrangement(V=ship_set,
                            E=sp_set,
                            L=shore_length,
                            d=d
                            )

    obj.arrange()


