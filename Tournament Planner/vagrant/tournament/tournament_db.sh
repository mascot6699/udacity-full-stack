

# Run this file to create a database first.
# Then run the tournament.sql to create tables.

# Drops table if it exists we can unncomment it if need be (ie running this script second time)

# dropdb tournament

# Creates a database named tournament.
# This will fail with an error if it exists --> "createdb: database creation failed: ERROR:  database "tournament" already exists"

echo "Creating a database in postgres for you"
createdb tournament
