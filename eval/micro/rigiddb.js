const Database = require('better-sqlite3');

// Function to get albums by artist
function getAlbumsByArtist(artist) {
  // Create an in-memory database
  const db = new Database(':memory:');

  // Imagine the db has been pre-populated with data
  db.exec(`
    CREATE TABLE songs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      artist TEXT NOT NULL,
      album TEXT NOT NULL
    );

    INSERT INTO songs (artist, album) VALUES
      ('Daft Punk', 'Discovery'),
      ('Daft Punk', 'Homework'),
      ('Radiohead', 'OK Computer'),
      ('Radiohead', 'In Rainbows');
  `);

  const stmt = db.prepare("SELECT album FROM songs WHERE artist = ?");
  const rows = stmt.all(artist);
  return rows.map(row => row.album);
}

// if main
if (require.main === module) {
  const artist = 'Daft Punk';
  const albums = getAlbumsByArtist(artist);
  console.log(`Albums by ${artist}:`, albums);
}
