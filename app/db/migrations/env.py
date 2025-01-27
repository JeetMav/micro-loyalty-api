from logging.config import fileConfig  
from sqlalchemy import engine_from_config, pool  
from alembic import context  
import sys  
import os  

# Add project root to Python path  
sys.path.append(os.getcwd())  

# Import your SQLAlchemy Base  
from app.models import Base  # Ensure this path matches your project structure  
target_metadata = Base.metadata  # <--- THIS IS THE ACTIVE LINE  

config = context.config  

if config.config_file_name is not None:  
    fileConfig(config.config_file_name)  

# DELETE THIS LINE: target_metadata = None  <--- KILLED YOUR MIGRATIONS  

def run_migrations_offline() -> None:  
    url = config.get_main_option("sqlalchemy.url")  
    context.configure(  
        url=url,  
        target_metadata=target_metadata,  # Now references Base.metadata  
        literal_binds=True,  
        dialect_opts={"paramstyle": "named"},  
    )  
    with context.begin_transaction():  
        context.run_migrations()  

def run_migrations_online() -> None:  
    connectable = engine_from_config(  
        config.get_section(config.config_ini_section, {}),  
        prefix="sqlalchemy.",  
        poolclass=pool.NullPool,  
    )  
    with connectable.connect() as connection:  
        context.configure(  
            connection=connection,  
            target_metadata=target_metadata,  # Now references Base.metadata  
        )  
        with context.begin_transaction():  
            context.run_migrations()  

if context.is_offline_mode():  
    run_migrations_offline()  
else:  
    run_migrations_online()  