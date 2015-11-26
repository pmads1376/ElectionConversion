import os

races = {}
newDir = os.path.join(os.getcwd(), "new")

for f in os.listdir(os.path.join(os.getcwd(), "Manual20130806")):

    try:
        if f in os.listdir(os.path.join(os.getcwd(), "20130806")):
            os.remove(os.path.join(os.getcwd(), "20130806/" + f))
    except Exception, e:
        print e
