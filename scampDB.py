import psycopg2
import psycopg2.extras

class DB:
    
    
    def __init__(self):
        self.conn = psycopg2.connect("dbname=scamp user=postgres password=king host=localhost")
        #self.conn = psycopg2.connect("dbname=scamp user=roxana password=Roxana-54321-Attar host=lamborghini.cs.uga.edu port=2200")
        self.cursors = dict()
        
        
    def tear_connection(self, commit=True):
        if commit:
            self.commit()
        for cur_name in self.cursors:
#             print "db_utils: closing cursor %s" % cur_name
            self.cursors[cur_name].close()
        self.conn.close()
        
    
    def commit(self):
#         print "db_utils: commit"
        self.conn.commit()
    
    
    def get_cursor(self, cur_name, dict_like=False):
        if dict_like:
            self.cursors[cur_name] = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        else:
            self.cursors[cur_name] = self.conn.cursor()
#         print "db_utils: cursor %s created" % cur_name
        return self.cursors[cur_name]
    
    
    def close_cursor(self, cur):
        for cur_name in self.cursors:
            if self.cursors[cur_name] == cur:
                self.cursors[cur_name].close()
                return
#         print "db_utils: couldn't find the cursor to close!"