from database import get_connection


def get_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%';
    """)

    tables = [row[0] for row in cursor.fetchall()]

    conn.close()

    return tables


def get_columns(table_name):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA table_info({table_name});")

    columns = cursor.fetchall()

    conn.close()

    return columns


def get_foreign_keys(table_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"PRAGMA foreign_key_list({table_name});")

    foreign_keys = cursor.fetchall()

    conn.close()

    return foreign_keys


def get_schema():

    schema = "DATABASE SCHEMA\n\n"

    tables = get_tables()

    for table in tables:

        schema += "=" * 60 + "\n"
        schema += f"TABLE: {table}\n"
        schema += "=" * 60 + "\n\n"

        columns = get_columns(table)

        schema += "Columns:\n"

        for column in columns:

            cid = column[0]
            name = column[1]
            dtype = column[2]
            not_null = column[3]
            default = column[4]
            pk = column[5]

            schema += f"- {name} ({dtype})"

            if pk:
                schema += " [PRIMARY KEY]"

            if not_null:
                schema += " [NOT NULL]"

            if default is not None:
                schema += f" DEFAULT={default}"

            schema += "\n"

        foreign_keys = get_foreign_keys(table)

        if foreign_keys:

            schema += "\nForeign Keys:\n"

            for fk in foreign_keys:

                referenced_table = fk[2]
                from_column = fk[3]
                to_column = fk[4]

                schema += (
                    f"- {from_column} -> "
                    f"{referenced_table}.{to_column}\n"
                )

        schema += "\n\n"

    return schema


if __name__ == "__main__":

    print(get_schema())