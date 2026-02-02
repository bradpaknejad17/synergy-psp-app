-- Initial SQLite schema for PSP app
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS psp (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  contract TEXT,
  vision TEXT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  status TEXT NOT NULL DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  psp_id INTEGER NOT NULL REFERENCES psp(id) ON DELETE CASCADE,
  description TEXT,
  category TEXT NOT NULL,
  start_date DATE NOT NULL,
  due_date DATE,
  completed_value REAL DEFAULT 0,
  target_value REAL DEFAULT 0,
  unit TEXT,
  completed INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_task_psp ON task(psp_id);
CREATE INDEX IF NOT EXISTS idx_task_due ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_psp_created ON psp(created_at DESC);
