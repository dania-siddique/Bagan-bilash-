from database import SessionLocal, add_plants, Base, engine

def main():
   
    Base.metadata.create_all(bind=engine)
    
    
    db = SessionLocal()
    
    try:
       
        add_plants(db)
        print("Plants have been successfully added to the database.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        
        db.close()

if __name__ == "__main__":
    main()