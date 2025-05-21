import pypyodbc 
def connect():
    driver = "{ODBC Driver 17 for SQL Server}"
    server = "DESKTOP-24QOS1E"
    db = "notebookAPI"
    user = "sa"
    password = "12345678"
    # remember to change infos above according to your own database
    request = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={db};
    UID={user};
    PWD={password};
    Trusted_Connection=yes;
    """

    con = pypyodbc.connect(request)
    return con