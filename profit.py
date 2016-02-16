from sqlalchemy.orm import sessionmaker
from bd_creation import engine
from bd_creation import Base, Difficulte, Electricite, Machine, Bitcoin

Base.metadata.bind = engine
session = sessionmaker(bind=engine)()

session.query(Difficulte).all()

NONCE = pow(2, 32)

# Nombre de bitcoins trouvés en moyenne pour un jour
bitcoins_par_jour = lambda h, d: (675 * h) / (33554432 * d)
# Coût en électricité par jour
cout_par_jour = lambda c, p: 24 * c * p


