import sys
sys.path.append("../")
from databaseInteraction import *
session=sessionmaker(engine)()
subs=session.query(Subscription).all()
for sub in subs:
    new_sub=New_Subscription(TelegramID=sub.TelegramID,
    Type=sub.Type,
    Start=sub.Start,
    End=sub.End,
    PayID=sub.PayID,
    AmountOfTry=sub.AmountOfTry
    
    )
    session.add(sub)
session.commit()


