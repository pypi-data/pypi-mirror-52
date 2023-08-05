import sys
class Argvreader:
    def __init__(self):
        self.argv = sys.argv
    
    @staticmethod
    def represents_int(candidate):
        if candidate[0] in ('-', '+'):
            return candidate[1:].isdigit()
        return candidate.isdigit()

    def get_argv_pairs(self, keylist=None):
        char_num_dict = {}
        if keylist is None:
            keylist = []
            for i, word in enumerate(self.argv[1: -1]):
                if word[0] == '-' and len(word) == 2 and self.represents_int(self.argv[i+2]):
                    keylist.append(word)
        
        for i, word in enumerate(self.argv[1: -1]):
            if word in keylist and self.represents_int(self.argv[i+2]):
                char_num_dict[word] = self.argv[i+2]
        
        if char_num_dict is 
        return char_num_dict


if __name__ == '__main__':
    A = Argvreader()
    print(A.get_argv_pairs())
    print(A.get_argv_pairs(['-m']))        
    
