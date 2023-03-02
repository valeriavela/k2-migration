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
                target_revenue_2023 numeric,
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
                website character varying(255),
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
                PRIMARY KEY (client_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS public.client_settlement (
                client_settlement_id uuid,
                client_id uuid,
                account_name character varying(255),
                clearing character varying(255),
                tax_id character varying(45),
                DTC integer,
                institution_id character varying(45),
                agent_bank_id character varying(45),
                account_number character varying(45),
                clearing_account_number character varying(45),
                occ character varying(45),
                created_at timestamp with time zone,
                updated_at timestamp with time zone,
                PRIMARY KEY (client_settlement_id),
                CONSTRAINT FK_client_settlement_client_id
                    FOREIGN KEY (client_id)
                    REFERENCES public.clients(client_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS public.epm_clients (
                client_id uuid,
                seller boolean,
                buyer boolean,
                company boolean,
                accredited_investors boolean,
                cost_basis numeric[],
                tax_year integer,
                suitability_docs boolean,
                crs_provided boolean,
                crs_conflict boolean,
                retail boolean,
                created_at timestamp with time zone,
                updated_at timestamp with time zone,
                PRIMARY KEY (client_id),
                CONSTRAINT FK_epm_clients_client_id
                    FOREIGN KEY (client_id)
                    REFERENCES public.clients(client_id)
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