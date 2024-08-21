import sqlite3
import os

class BCCWJSources(object):

    def __init__(self):
        self.conn = sqlite3.connect("bccwjsources.db")
        self.divide_sources()


    #def __del__(self):
    #    self.conn.close()


    def query_many(self, fields="*", constraint=None):
        if constraint is None:
            for row in self.conn.execute("select {} from sources".format(",".join(fields))):
                yield row
        else:
            for row in self.conn.execute("select {} from sources where {}".format(",".join(fields), constraint)):
                yield row


    def divide_sources(self):
        """Divide sources according to corpus, genre etc.

        """

        #corpora = set([name[0:2] for query_result in self.conn.execute("SELECT sample_id FROM sources GROUP BY sample_id ORDER BY sample_id") for name in query_result])
        #for corpus in corpora:
        #    genres = set([genre for query_result in self.conn.execute("SELECT genre_1 FROM sources WHERE (sources.sample_id LIKE \"%{}%\") GROUP BY genre_1 ORDER BY genre_1".format(corpus)) for genre in query_result])
        #    for genre in genres:
        #        genres_2 = set([genre for query_result in self.conn.execute("SELECT genre_2 FROM sources WHERE (sources.sample_id LIKE \"%{}%\") GROUP BY genre_2 ORDER BY genre_2".format(corpus)) for genre in query_result])
        #        for subgenre in genres_2:
        #            print(corpus, genre, subgenre)



if __name__ == "__main__":
    if os.path.exists("bccwjsources.db"):
        os.remove("bccwjsources.db")
    conn = sqlite3.connect("bccwjsources.db")
    conn.execute("""CREATE TABLE sources(
sample_id PRIMARY KEY,
bib_id,
title,
subtitle,
number,
bib_author,
publisher,
year,
isbn,
size,
pages,
genre_1,
genre_2,
genre_3,
genre_4,
bib_author_id,
sampling_page,
sampling_point,
status,
core,
author_id,
author,
sex,
birthyear
)""")

    with open("Join_all.txt", "r") as f:
        # Fill the table
        for line in f:
            #print(line)
            conn.execute("INSERT INTO sources VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line.rstrip("\n").split("\t"))

    # Print the table contents
    for row in conn.execute("SELECT sample_id, author FROM sources"):
        print(row)

    conn.commit()
    conn.close()
