// A tiny browser service, port 4032, like AgentCore Browser:
// each session is a fresh, isolated browser, controlled over HTTP.
const { chromium } = require("playwright-core");
const http = require("node:http");

const sessions = {};  // session id -> an isolated browser page
let browser;
let shots = 0;

const actions = {
  async start() {
    const id = `session-${Object.keys(sessions).length + 1}`;
    const context = await browser.newContext({
      viewport: { width: 1280, height: 720 } });  // isolated
    sessions[id] = await context.newPage();
    return { session: id };
  },
  async goto(page, q) {
    await page.goto(q.url);
    return { opened: q.url, sees: await page.innerText("body") };
  },
  async type(page, q) {
    await page.getByLabel(q.field).fill(q.text);
    return { typed: q.text, into: q.field };
  },
  async click(page, q) {
    await page.getByRole("button", { name: q.button }).click();
    await page.waitForLoadState();
    return { clicked: q.button, sees: await page.innerText("body") };
  },
  async read(page) {
    return { text: await page.innerText("body") };
  },
};

http.createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");
  const q = Object.fromEntries(url.searchParams);
  if (url.pathname.startsWith("/shot/")) {  // a saved screenshot
    res.writeHead(200, { "Content-Type": "image/png" });
    return require("node:fs").createReadStream(
      `${__dirname}/shots${url.pathname.slice(5)}`).pipe(res);
  }
  const name = url.pathname.slice(1);
  const page = sessions[q.session];
  page?.setDefaultTimeout(3000);  // fail fast, never hang
  let result;
  try {
    result = await actions[name](page, q);
  } catch (error) {  // the agent gets the error and can retry
    result = { error: error.message.split("\n")[0] };
  }
  if (page) {  // a screenshot after every action: our "live view"
    shots += 1;
    const file = `${__dirname}/shots/${shots}.png`;
    await page.screenshot({ path: file });
    result.screenshot = `http://localhost:4032/shot/${shots}.png`;
  }
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify(result));
}).listen(4032, async () => {
  browser = await chromium.launch();
  console.log("Browser service on http://localhost:4032");
});
