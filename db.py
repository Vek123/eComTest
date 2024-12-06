from tinydb import TinyDB


db = TinyDB("db.json")
table = db.table("schemas")


def get_schemas():
    return table.all()


def fill_table(table):
    table.insert(
        {
            "name": "Form email_phone_date",
            "email_field": "email",
            "phone_field": "phone",
            "text_field": "text",
            "date_field": "date",
        }
    )
    table.insert(
        {
            "name": "Form email_phone_text",
            "email_field": "email",
            "phone_field": "phone",
            "text_field": "text",
        }
    )
    table.insert(
        {
            "name": "Form phone",
            "phone_field": "phone",
        }
    )
    table.insert(
        {
            "name": "Form email",
            "email_field": "email",
        }
    )
    table.insert(
        {
            "name": "Form phone_email",
            "phone_field": "phone",
            "email_field": "email",
        }
    )
    table.insert(
        {
            "name": "Form date",
            "date_field": "date",
        }
    )
    table.insert(
        {
            "name": "Form date_text",
            "date_field": "date",
            "text_field": "text",
        }
    )
    table.insert(
        {
            "name": "Form text",
            "text_field": "text",
        }
    )
    table.insert(
        {
            "name": "Form email_date",
            "email_field": "email",
            "date_field": "date",
        }
    )


if __name__ == "__main__":
    fill_table(table)
