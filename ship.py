

class Ship():
    def __init__(self, length, arrive_time, process_time, support_sp,
                 engine_power_coeff, engine_power, engine_fuel_consumption):
        ## fixed ship info 
        self.l = length
        self.arrive_time = arrive_time
        self.process_time = process_time
        self.support_sp = support_sp
        
        self.engine_power_coeff = engine_power_coeff
        self.engine_power = engine_power
        self.engine_fuel_consumption = engine_fuel_consumption
        
        ## 
        self.isfinished = False
        self.berth_location = None
        self.record = []
        
    def operate(self, start_time, end_time, use_sp):
        operation_time = end_time - start_time
        
        self.record.append({
            "start_time": start_time,
            "end_time": end_time,
            "operation_time": operation_time,
            "use_sp": use_sp
            })