import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://billinguser:mc6BRfIRg4VPXkb11eR6ezCNYZV5BIAS@dpg-d02fk4euk2gs73eec590-a.frankfurt-postgres.render.com:5432/billingdb_5gyy")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret")
    JWT_HEADER_TYPE = "Bearer"
