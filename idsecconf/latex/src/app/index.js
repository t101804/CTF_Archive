const express = require("express");
const bodyParser = require("body-parser");
const { marked } = require("marked");
const createDOMPurify = require("dompurify");
const { JSDOM } = require("jsdom");
const Database = require("better-sqlite3");
const path = require("path");
const app = express();
const { v4: uuidv4 } = require("uuid");
const dotenv = require("dotenv");
const crypto = require("crypto");
const session = require("express-session");
const SQLiteStore = require("connect-sqlite3")(session);
const cookieParser = require("cookie-parser");
const fs = require("fs");

dotenv.config();

const procenv = process.env;
const port = procenv.PORT || 3000;

app.set("view engine", "ejs");
app.use(express.static("public"));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

function generateCSRFToken() {
  return crypto.randomBytes(32).toString("hex");
}

app.set("trust proxy");
app.use(
  session({
    cookie: { maxAge: 300000 },
    store: new SQLiteStore({
      db: "./sessions.db",
      concurrentDB: "true",
    }),
    secret: procenv.SESSIONSECRET || "ilysm",
    resave: false,
    saveUninitialized: true,
  })
);

const authToken = procenv.TOKEN || "ilysm";

app.use((req, res, next) => {
  const csrfToken = generateCSRFToken();
  if (!req.session.csrfToken) req.session.csrfToken = csrfToken;
  next();
});

if (!fs.existsSync(path.join(__dirname, "database")))
  fs.mkdirSync(path.join(__dirname, "database"));
const db = new Database(path.join(__dirname, "database", "questions.db"));
db.exec(`
  CREATE TABLE IF NOT EXISTS questions (
    id TEXT PRIMARY KEY,
    content TEXT,
    answer TEXT,
    is_answered BOOLEAN,
    created_at INTEGER
  )
`);

function clearOldQuestions() {
  const oneHourAgo = Date.now() - 300000;
  const deleteOldQuestions = db.prepare(
    "DELETE FROM questions WHERE created_at < ?"
  );
  const info = deleteOldQuestions.run(oneHourAgo);
  console.log(`Cleared ${info.changes} old questions`);
}

setInterval(clearOldQuestions, 300000);

app.get("/", (req, res) => {
  const questions = db
    .prepare("SELECT * FROM questions ORDER BY created_at DESC LIMIT 20")
    .all();
  res.render("index", {
    questions,
    astolfoToken: req.cookies
      ? req.cookies.astolfoToken === authToken
      : undefined,
  });
});

app.post("/ask", (req, res) => {
  const { content } = req.body;
  const createdAt = Date.now();
  const id = uuidv4();
  const insert = db.prepare(
    "INSERT INTO questions (id, content, is_answered, created_at) VALUES (?, ?, 0, ?)"
  );
  insert.run(id, content, createdAt);
  res.redirect(`/question/${id}`);
});

app.get("/question/:id", (req, res) => {
  const id = req.params.id;
  const question = db.prepare("SELECT * FROM questions WHERE id = ?").get(id);
  if (question) {
    const window = new JSDOM("").window;
    const DOMPurify = createDOMPurify(window);
    question.content = DOMPurify.sanitize(
      marked(question.content, { pedantic: true })
    );
    if (question.answer) {
      question.answer = marked(question.answer, { pedantic: true });
    }
    // console.log(req.cookies);
    res.render("question", {
      question,
      astolfoToken: req.cookies
        ? req.cookies.astolfoToken === authToken
        : undefined,
      csrfToken: req.session.csrfToken,
    });
  } else {
    res.status(404).send("Question not found");
  }
});

app.get("/api/unanswered-questions", (req, res) => {
  if (req.cookies.astolfoToken !== authToken) {
    return res.status(403).send("Unauthorized");
  }

  const unansweredQuestions = db
    .prepare(
      "SELECT id, content FROM questions WHERE is_answered = 0 ORDER BY created_at DESC"
    )
    .all();

  res.json(unansweredQuestions);
});

app.post("/question/:id/answer", (req, res) => {
  const { id } = req.params;
  const { answer } = req.body;

  if (
    req.session.csrfToken !== req.body._csrf ||
    req.cookies.astolfoToken !== authToken
  ) {
    return res.status(403).send("Unauthorized");
  }

  db.prepare(
    "UPDATE questions SET answer = ?, is_answered = 1 WHERE id = ?"
  ).run(answer, id);
  res.redirect(`/question/${id}`);
});

app.get("/admin/flag", (req, res) => {
  if (req.cookies.astolfoToken === authToken) {
    res.json({ flag: procenv.FLAG || "flag{placeholder}" });
  } else {
    res.status(403).send("Unauthorized");
  }
});

app.listen(port, () => {
  console.log(`App listening at port ${port}`);
});
