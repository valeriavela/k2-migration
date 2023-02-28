import psycopg
from config import config


def create_client_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE clients (
                client_id uuid PRIMARY KEY,
                salesforce_account_owner character varying(45),
                name character varying(255),
                "Description" text,
                "Billing State/Province" character varying(255),
                "Last Modified Date (SF)" timestamp,
                "Created Date (SF)" timestamp,
                "Account ID (SF)" character varying(45),
                "2023 Target Revenue" numeric,
                "Billing Country" character varying(255),
                "Billing Zip/Postal Code" character varying(45),
                "Account Gameplan" text,
                "Account Status" character varying(45),
                "Account Structure" character varying(255),
                "Client Category" character varying(255),
                "CRD  Number" character varying(255),
                "Date Opened" date,
                "Elevation Coverage" character varying(255),
                "Elevation Coverage 1" character varying(255),
                "Elevation Coverage 1 Asset Class" character varying(255),
                "Elevation Coverage 2" character varying(255),
                "Elevation Coverage 2 Asset Class" character varying(255),
                "Elevation Coverage 3" character varying(255),
                "Elevation Coverage 3 Asset Class" character varying(255),
                "Elevation Product Interest" character varying(255),
                "Is Account Closed" boolean,
                "Notes" text,
                "Open to Trade Options" boolean,
                "SEC Number" character varying(255),
                "Scheduled Research Calls" character varying(255),
                "Broker Dealer" boolean,
                "Large Trader Name" character varying(255),
                "LTID" character varying(255),
                "LEI Number" character varying(255),
                "Authorized Traders" text,
                "Operations Email" character varying(255),
                "Operations Contact" character varying(255),
                "Compliance Email" character varying(255),
                "Compliance Contact" character varying(255),
                "Tax ID" character varying(255),
                "OFAC" boolean,
                "FinCen" boolean,
                "created_at" timestamp with time zone,
                "updated_at" timestamp with time zone,
                PRIMARY KEY ("client_id")
        );

        CREATE TABLE "Client settlement" (
                "settlement_id" uuid,
                "client_id" uuid,
                "account name" character varying(255),
                "side" character varying(255),
                "tax ID" character varying(45),
                "clearing" character varying(255),
                "DTC" int,
                "institution ID" int,
                "agent bank ID" int,
                "account number" character varying(45),
                "CMTA" character varying(45),
                "CUID" character varying(45),
                "notes" text,
                "country" character varying(45),
                "created_at" timestamp with time zone,
                "updated_at" timestamp with time zone,
                PRIMARY KEY ("settlement_id"),
                CONSTRAINT "FK_Client settlement.client_id"
                    FOREIGN KEY ("client_id")
                    REFERENCES "client"("client_id")
        );
        """
        """
        CREATE TABLE "client_interaction" (
                "salesforce_id" character(15),
                "client_id" uuid,
                "name" character varying(255),
                "analyst on interaction" character varying(255),
                "date" date,
                "days since last interaction" numeric,
                "deal interest" text,
                "flow interactions" numeric,
                "notes" text,
                "notification" character varying(45),
                "primary contacts in interaction" character varying(45),
                "secondary contacts in interaction" character varying(45),
                "resource or relationship interaction" USER-DEFINED,
                "time spent(minutes)" numeric,
                "salesperson" uuid,
                "type of interaction" character varying(255),
                "value added interaction" boolean,
                "created by (SF)" character varying(45),
                "created date (SF)" date,
                "last modified date (SF)" date,
                "created_at" timestamp with time zone,
                "updated_at" timestamp with time zone,
                PRIMARY KEY ("salesforce_id"),
                CONSTRAINT "FK_client_interaction.salesperson"
                    FOREIGN KEY ("salesperson")
                    REFERENCES "salesperson"("salesperson_id"),
                CONSTRAINT "FK_client_interaction.client_id"
                    FOREIGN KEY ("client_id")
                    REFERENCES "client"("client_id")
        );
        """

        """
        CREATE TABLE "Elevation Private Markets Clients" (
                "client_id" uuid,
                "seller" boolean,
                "buyer" boolean,
                "company" boolean,
                "accredited investors" boolean,
                "cost basis" int[],
                "tax year" date,
                "suitability" boolean,
                "CRS provided" boolean,
                "CRS conflict" boolean,
                "individual" boolean,
                "created_at" timestamp with time zone,
                "updated_at" timestamp with time zone,
                PRIMARY KEY ("client_id")
        );
        """

        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_client_tables()