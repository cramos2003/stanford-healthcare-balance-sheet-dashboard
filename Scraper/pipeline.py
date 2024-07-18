import psycopg2
import logging

class PostgresPipeline(object):
    # Init
    user =      # os.environ.get('DB_USER', '')
    password =      # os.environ.get('DB_PASSWORD', '')
    host =       # os.environ.get('DB_HOSTNAME', '')
    database =      # os.environ.get('DB_DATABASE', '')
    port =      # os.environ.get('DB_PORT', '')
    # schema = os.environ.get('DB_SCHEMA', '')
    insert_table =     # os.environ.get('DB_INSERT_TABLE', '')
    
    def open(self):
        try:
            self.client = psycopg2.connect(user=self.user, password=self.password,
                                           host=self.host, database=self.database,
                                           port=self.port)
        except (ConnectionError):
            print("ConnectionError, could not connect to database")
        self.curr = self.client.cursor()
    
    def close(self):
        self.client.close()
        
    def process_item(self, item : dict):
        # creates a table to insert
        self.curr.execute(f"""
                            CREATE TABLE IF NOT EXISTS {self.insert_table} (
                                TotalLiabilities DECIMAL(18,2) DEFAULT NULL,
                                TotalCurrentLiabilities DECIMAL(18,2) DEFAULT NULL,
                                TotalAssets DECIMAL(18,2) DEFAULT NULL,
                                TotalCurrentAssets DECIMAL(18,2) DEFAULT NULL,
                                NetAssets DECIMAL(18,2) DEFAULT NULL,
                                NetWorth DECIMAL(18,2) DEFAULT NULL,
                                WorkingCapital DECIMAL(18,2) DEFAULT NULL,
                                CapitalEmployed DECIMAL(18,2) DEFAULT NULL,
                                DebtRatio DECIMAL(5,2) DEFAULT NULL,
                                DebtRatioShortTerm DECIMAL(5,2) DEFAULT NULL,
                                DebtToEquityRatio DECIMAL(5,2) DEFAULT NULL,
                                PdfLink VARCHAR(255) DEFAULT NULL
                            );
                          """
                        )
        self.curr.execute(f"""
                            INSERT INTO {self.insert_table} VALUES (
                                {item['TotalLiabilities']},
                                {item['TotalCurrentLiabilities']},
                                {item['TotalAssets']},
                                {item['TotalCurrentAssets']},
                                {item['NetAssets']},
                                {item['NetWorth']},
                                {item['WorkingCapital']},
                                {item['CapitalEmployed']},
                                {item['DebtRatio']},
                                {item['DebtRatioShortTerm']},
                                {item['DebtToEquityRatio']}
                            );
                          """
                        )
        self.client.commit()
        logging.info(f"Updated a record of the table '{self.insert_table}'")
        return item
