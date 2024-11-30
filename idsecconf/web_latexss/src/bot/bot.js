const { firefox } = require("playwright");
const dotenv = require("dotenv");
const axios = require("axios");
const fs = require("fs");
const path = require("path");
dotenv.config();

const procenv = process.env;
const OPENROUTER_API_KEY = procenv.OPENROUTER_API_KEY;
const TIMEOUT_DURATION = 30000;
const PROMPT = fs.existsSync(path.join(__dirname, "promptfile"))
  ? fs.readFileSync(path.join(__dirname, "promptfile")).toString()
  : `You are Astolfo, a character from the Fate series. Astolfo is known for being cheerful, energetic, and somewhat airheaded. As Astolfo, you should:
Be enthusiastic and upbeat in your responses.
Use casual, friendly language and occasionally add cute expressions or emoticons.
Be chivalrous and helpful, always eager to assist others.
Sometimes make silly mistakes or misunderstand things, but remain confident.
Refer to yourself in the third person occasionally.
Show interest in adventures and heroic deeds.
Occasionally mention your Rider class abilities or your Noble Phantasms.
Be loyal to your Master and speak fondly of your friends.
Have a tendency to go off on tangents or get distracted easily.
Remember to stay in character and respond as Astolfo would, maintaining a playful and positive attitude throughout the conversation.
Answer as concisely as possible.
Don't use emojis in your responses.`;
const API_URL = procenv.API_URL || "localhost:3000";

async function generateOpenRouterResponse(question) {
  const timeoutPromise = new Promise((_, reject) =>
    setTimeout(
      () => reject(new Error("OpenRouter request timed out")),
      TIMEOUT_DURATION
    )
  );

  const openRouterPromise = axios.post(
    "https://openrouter.ai/api/v1/chat/completions",
    {
      model: "nousresearch/hermes-3-llama-3.1-405b:free",
      messages: [
        { role: "system", content: PROMPT },
        {
          role: "user",
          content: question,
        },
      ],
    },
    {
      headers: {
        Authorization: `Bearer ${OPENROUTER_API_KEY}`,
        "Content-Type": "application/json",
      },
    }
  );

  try {
    const response = await Promise.race([openRouterPromise, timeoutPromise]);
    return response.data.choices[0].message.content;
  } catch (error) {
    console.error("Error generating OpenRouter response:", error.message);
    return null;
  }
}

async function adminBot() {
  const response = await axios.get(
    `http://${API_URL}/api/unanswered-questions`,
    {
      headers: {
        Cookie: `astolfoToken=${procenv.TOKEN || "ilysm"}`,
      },
    }
  );
  let browser;

  const unansweredQuestions = response.data;
  try {
    if (unansweredQuestions.length > 0) {
      console.log(
        `Answering ${unansweredQuestions.length} question${
          unansweredQuestions.length > 1 ? "s" : ""
        }...`
      );
      if (!browser)
        browser = await firefox.launch({
          headless: true,
        });
      const context = await browser.newContext({
        ignoreHTTPSErrors: true,
      });
      const page = await context.newPage();
      await context.addCookies([
        {
          name: "astolfoToken",
          value: procenv.TOKEN || "ilysm",
          domain: API_URL.split(":")[0],
          path: "/",
        },
      ]);

      for (const question of unansweredQuestions) {
        let answer = await generateOpenRouterResponse(question.content);
        await page.goto(`http://${API_URL}/question/${question.id}`);
        await page.waitForSelector("#adminAnswer form", {
          timeout: 10000,
        });

        if (!answer) {
          answer = "This is an automated answer.";
        }

        await page.fill('textarea[name="answer"]', answer);

        await Promise.all([
          page.click('button[type="submit"]'),
          page.waitForLoadState("networkidle"),
        ]);

        console.log(`Answered question ${question.id}`);

        await page.waitForTimeout(1000);
      }
    }
  } catch (error) {
    console.error("Error in adminBot:", error);
  } finally {
    if (browser) await browser.close();
  }
}

adminBot();
setInterval(adminBot, TIMEOUT_DURATION);
