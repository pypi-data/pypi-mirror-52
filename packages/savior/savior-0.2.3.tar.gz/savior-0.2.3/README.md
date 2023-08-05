# Savior Database

Embedded schema-less database library backed by LMDB.

Currently in development and not stable yet. 
The interface and disk format may change in future versions without notice.
You probably shouldn't use it to store important data. 

Permissively licensed with the [ISC License](LICENSE).

## Goals

- provide a language-neutral disk format
- utilize LMDB's properties like transactions, append-only writes, and zero-copy reads
- provide intuitive schema-less entity modeling and querying interface
- store an immutable history of all values in the database

## Developer Interface

There are a few actions you can perform on entities in a transaction:

- store
- fetch
- update
- query
- delete

An entity is conceptually like a dictionary with attributes and values.

A table is an isolated section of the database for storing entities,
usually with a similar set of attributes.

## Disk Format

All entities of the same type are stored in one inner LMDB database
There is no guarantee that entities have a consistent schema.

Entities are stored on disk as a series of timestamped attribute changes.

- key-value entries have the form `(uuid, timestamp, attribute) -> value`
- `uuid` is an auto-generated entity ID
- `timestamp` is an auto-generated timestamp of when the entry was appended
- `attribute` and `value` are the updated entity key value entries

Data is not modified for updates, only appended to indicate the entity changed.

The storage format version is stored as an integer in a special inner database 
named `_metadata`, at a key named `version`. 
The `_metadata` table's keys and values are also encoded with MessagePack.

You can access the storage format version via `Database.VERSION`.

