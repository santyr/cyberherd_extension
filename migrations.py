from lnbits.helpers import urlsafe_short_hash

async def m001_initial(db):
    """
    Initial cyberherd payment table.
    """
    # Check if the table already exists
    exists = await db.fetchone("SELECT to_regclass('cyberherd.targets')")
    if not exists:
        await db.execute(
            """
            CREATE TABLE cyberherd.targets (
                wallet TEXT NOT NULL,
                source TEXT NOT NULL,
                percent INTEGER NOT NULL CHECK (percent >= 0 AND percent <= 100),
                alias TEXT,
                UNIQUE (source, wallet)
            );
            """
        )

async def m002_float_percent(db):
    """
    Add float percent and migrates the existing data.
    """
    await db.execute("ALTER TABLE cyberherd.targets RENAME TO cyberherd_old")
    await db.execute(
        """
        CREATE TABLE cyberherd.targets (
            wallet TEXT NOT NULL,
            source TEXT NOT NULL,
            percent REAL NOT NULL CHECK (percent >= 0 AND percent <= 100),
            alias TEXT,
            UNIQUE (source, wallet)
        );
        """
    )

    for row in [
        list(row)
        for row in await db.fetchall("SELECT * FROM cyberherd.cyberherd_old")
    ]:
        await db.execute(
            """
            INSERT INTO cyberherd.targets (
                wallet,
                source,
                percent,
                alias
            )
            VALUES (?, ?, ?, ?)
            """,
            (row[0], row[1], row[2], row[3]),
        )

    await db.execute("DROP TABLE cyberherd.cyberherd_old")

async def m003_add_id_and_tag(db):
    """
    Add float percent and migrates the existing data.
    """
    await db.execute("ALTER TABLE cyberherd.targets RENAME TO cyberherd_old")
    await db.execute(
        """
        CREATE TABLE cyberherd.targets (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            source TEXT NOT NULL,
            percent REAL NOT NULL CHECK (percent >= 0 AND percent <= 100),
            tag TEXT NOT NULL,
            alias TEXT,
            UNIQUE (source, wallet)
        );
        """
    )

    for row in [
        list(row)
        for row in await db.fetchall("SELECT * FROM cyberherd.cyberherd_old")
    ]:
        await db.execute(
            """
            INSERT INTO cyberherd.targets (
                id,
                wallet,
                source,
                percent,
                tag,
                alias
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (urlsafe_short_hash(), row[0], row[1], row[2], "", row[3]),
        )

    await db.execute("DROP TABLE cyberherd.cyberherd_old")

async def m004_remove_tag(db):
    """
    This removes the 'tag' column.
    """
    keys = "id, wallet, source, percent, alias"
    new_db = "cyberherd.targets"
    old_db = "cyberherd.targets_old"

    await db.execute(f"ALTER TABLE {new_db} RENAME TO targets_old")
    await db.execute(
        f"""
        CREATE TABLE {new_db} (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            source TEXT NOT NULL,
            percent REAL NOT NULL CHECK (percent >= 0 AND percent <= 100),
            alias TEXT,
            UNIQUE (source, wallet)
        );
        """
    )
    await db.execute(f"INSERT INTO {new_db} ({keys}) SELECT {keys} FROM {old_db}")
    await db.execute(f"DROP TABLE {old_db}")

