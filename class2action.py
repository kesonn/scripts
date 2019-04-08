def user(c):
    def F(s,f):
        return c(s,f)
    return F

class Api(object):
    action = {}
    def __init__(self,token=None):
        self.token = token

    @classmethod
    def auth(self,k):
        if k==2:
            return 1
        return

    def do(self,act,kv):
        return getattr(self,act)(kv)

    @user
    def action(self,kv):
        print kv
        return 'sdfffsgf'+self.token

print Api('123234324').do('action',2)
