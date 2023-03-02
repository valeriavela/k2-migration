import psycopg
from config import config


def create_client_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE IF NOT EXISTS public.clients (
                client_id uuid NOT NULL,
                salesforce_account_owner character varying(45),
                salesforce_account_id character varying(18),
                salesforce_created timestamp,
                salesforce_last_modified timestamp,
                name character varying(255),
                description text,
                2023_target_revenue numeric,
                billing_state character varying(255),
                billing_country character varying(255),
                billing_zip_code character varying(45),
                account_gameplan text,
                account_status character varying(45),
                account_structure character varying(45),
                client_category character varying(45),
                crd_number integer,
                date_opened timestamp,
                elevation_coverage character varying(255),
                elevation_coverage_1 character varying(255),
                elevation_coverage_1_asset_class character varying(255),
                elevation_coverage_2 character varying(255),
                elevation_coverage_2_asset_class character varying(255),
                elevation_coverage_3 character varying(255),
                elevation_coverage_3_asset_class character varying(255),
                elevation_product_interest character varying(255),
                is_account_closed boolean,
                notes text,
                open_to_trade_options boolean,
                phone character varying(31),
                sec_number character varying(31),
                scheduled_research_calls character varying(255),
                website character varying(255)
                broker_dealer boolean,
                large_trader_name character varying(255),
                ltid character varying(45),
                lei_number character(20),
                authorized_traders text[],
                operations_email character varying(255),
                operations_contact character varying(255),
                compliance_email character varying(255),
                compliance_contact character varying(255),
                tax_id character varying(45),
                ofac boolean,
                fincen boolean,
                suitability boolean,
                created_at timestamp with time zone,
                updated_at timestamp with time zone,
                PRIMARY KEY ("client_id")
        )
        """,
        """
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