             
 
                                                                        
 
                                                                              
                                                                               
                                                                              
                                                                           
                                                                       
                                                          
 
                                                                            
                                                     
 
                                                                            
                                                                          
                                                                              
                                                                        
                                                                               
                                                                           
               
import math


def truncate(str_, length, separator="..."):
    """Truncates a string to the given length by removing internal characters.

    :param str_: The string to truncate.
    :param length: The length to truncate the string to.
    :param separator: The intermediary characters that replaces removed characters.
    """
    if len(str_) <= length:
        return str_

    start = math.ceil((length - len(separator)) / 2)
    end = math.floor((length - len(separator)) / 2)
    return f"{str_[:start]}{separator}{str_[len(str_) - end:]}"
