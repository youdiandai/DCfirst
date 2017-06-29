from hello import Major,db
f= open('major.txt')
for x in f:
    db.session.add(Major(mname=x[:-1]))
db.session.commit()