                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
                                                              


class HyperParameters(object):
    """Hyperparameters for RL agent"""

    def __init__(self):
                        
        self.ego_feature_num = 4
        self.npc_num = 5
        self.npc_feature_num = 5

        self.state_size = self.ego_feature_num + self.npc_num * self.npc_feature_num
        self.mask_size = self.npc_num + 1
        self.task_size = 4

        self.all_state_size = self.state_size + self.mask_size + self.task_size
        self.action_size = 2

                             
        self.noised_episodes = 2500        
        self.max_steps = 500       
        self.batch_size = 256       
        self.train_frequency = 2

                     
        self.tau = 1e-3

                                    
        self.lra = 2e-5
        self.lrc = 1e-4
        self.gamma = 0.99                    
        self.pretrain_length = 2500                                                                                                  
        self.buffer_size = (
            100000                                                              
        )
        self.load_buffer = (
            True                                                                
        )
        self.buffer_load_path = "memory_buffer/memory.pkl"
        self.buffer_save_path = "memory_buffer/memory.pkl"

                      
        self.model_save_frequency = 10
        self.model_save_frequency_no_paste = 50
