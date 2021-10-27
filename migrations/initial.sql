CREATE TABLE "transactions" (
	"id"	INTEGER NOT NULL UNIQUE,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"token_from"	TEXT NOT NULL,
	"amount_from"	REAL NOT NULL,
	"token_to"	TEXT NOT NULL,
	"amount_to"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)