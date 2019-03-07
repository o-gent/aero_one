import xlwings as xw

class Display():
    def __init__(self):
        self.wb = xw.Book('main.xlsx')
        self.main = self.wb.sheets['main']
        self.raw = self.wb.sheets['raw']
        id_list = {}
        self.latency = 0

    def refresh(self, data):
        """
        puts new data in 'raw' sheet for each call
        """
        try:
            # set latency on main screen
            self.raw.range(1,1).value = self.latency

            self.data = data

            x = self.raw.range
            data_sorted = sorted(self.data) # list of IDS present

            for entry in data_sorted:
                x(entry + 1, 2).value = entry # set each row first column with ID 
                
                i = 3 # set column index for next loop
                for value in self.data[entry]['payload']:
                    # go though the sorted array for ID
                    x(entry + 1, i).value = value
                    i += 1
        except:
            pass

    def value_history(self, id_list):
        """
        keeps a history of a variable for use in time graphs
        """
        for id_ in id_list:
            self.raw.range(id_, 2).value = id_
            id_list[id_] = [id_list[id_] , data[id_]['payload']]
            