class LoadBalancer:

    def __init__(self, servers):
        self.servers = servers
        self.pointer = 0 
        self.number_of_servers = len(servers)

    def get_next_server(self):
        choosen = self.servers[self.pointer]
        self.pointer = (self.pointer+1) % self.number_of_servers
        return choosen 
        
        


