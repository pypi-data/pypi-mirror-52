import peewee

# Late initialization in __main__
database = peewee.SqliteDatabase(None)


class BlockEntry(peewee.Model):
    decree = peewee.CharField()
    date = peewee.DateField()
    issuer = peewee.CharField()

    class Meta:
        database = database
        db_table = 'block_entries'


class BlockURL(peewee.Model):
    url = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_urls'


class BlockDomain(peewee.Model):
    domain = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_domains'


class BlockAddress(peewee.Model):
    address = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_addresses'
