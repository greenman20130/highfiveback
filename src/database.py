# import datetime
# from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, Boolean

# metadata = MetaData()

# company = Table(
#     "company",
#     metadata,
#     Column("id", String, primary_key=True),
#     Column("name", String),
#     Column("city", String),
# )

# user = Table(
#     "user",
#     metadata,
#     Column("user_id", String, primary_key=True),
#     Column("company_id", String, ForeignKey("company.id")),
#     Column("access_token", String,),
#     Column("name", String, nullable=False),
#     Column("last_name", String, nullable=False),
#     Column("photo", String),
#     Column("email", String, nullable=False),
#     Column("date_joined", TIMESTAMP, default=datetime.utcnow),
#     Column("hash_password", String, nullable=False),
#     Column("is_hr", Boolean, default=False),
# )
