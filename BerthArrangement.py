from ship import Ship
from sp import SP
from data_loader import DataLoader
from model import Model

from params import Params

class BerthArrangement():
    def __init__(self, V, L, E):
        self.V = V
        self.L = L      # shore length
        self.E = E      # shore power(sp) set
        
        self.params = Params()
    
    def adjust(self, b, s):
        assert len(b) == len(self.V)
        assert len(s) == len(self.V)
        
        # TODO
        pass


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


    def get_score(self):
        total_efficiency_score = 0
        emissions = 0
        
        for ship in self.V:
            total_efficiency_score += ship.record[-1]["end_time"] - ship.arrive_time
            
            engine_rate = ship.engine_power * ship.engine_power_coeff * ship.engine_fuel_consumption
            for each in ship.record:
                if each["use_sp"]:
                    emissions += each["operation_time"] * engine_rate
        
        total_emission_score = emissions * sum(w_p * c_p for w_p, c_p in zip(self.params.w, self.params.C))
            
        return total_efficiency_score, total_emission_score

    
    def compare(self, efficiency1, emission1, efficiency2, emission2):
        return efficiency1 + emission1 < efficiency2 + emission2
    
    
    def arrange(self):
        # TODO
        # get decision variables ---------
        b = None
        s = None
        # --------------------------------
        
        
        ## process
        b, s = self.adjust(b, s)
        
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
                
        self.efficiency_score, self.emmision_score = self.get_score()
        
        # sort
        rearrange_times = sorted(rearrange_times, key=lambda x: x[0])
        
        ## rearrange
        i = 0
        while i < len(rearrange_times):
            time, idx = rearrange_times[i]
            
            if self.need_rearrange():
                # update status
                self.V[idx].isfinished = True
                # multiple ships finish at the same time
                while rearrange_times[i+1][0] == time:
                    i += 1
                    idx = rearrange_times[i][1]
                    self.V[idx].isfinished = True
                
                new_efficiency, new_emission, new_rearrange_times = self.rearrange(time)
                if self.compare(self.efficiency_score, self.emmision_score, new_efficiency, new_emission):
                    self.efficiency_score = new_efficiency
                    self.emmision_score = new_emission
                    # update rearrange_times
                    rearrange_times = new_rearrange_times
                    i = 0
            i += 1
                
        return self.efficiency_score, self.emmision_score

            
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
        new_b, new_s = self.adjust(new_b, new_s)
        
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
                
            start_time = time + start_time
            end_time = start_time + ship.process_time
            rearrange_times.append((end_time, idx))
            
            if ship.support_sp and self.E.is_avaliable(berth_location):
                use_sp = True
            else:
                use_sp = False
                
            ship.operate(start_time, end_time, use_sp)
            
        efficiency_score, emmision_score = self.get_score()
        
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


