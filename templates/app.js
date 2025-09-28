const fs = require("fs");

// Read JSON file
const data = JSON.parse(fs.readFileSync("quiz.json", "utf8"));

// Print stack questions
console.log("📘 Stack Questions:");
data.stack.forEach((q, i) => {
    console.log(`${i + 1}. ${q.question}`);
    console.log("Options:", q.options.join(", "));
    console.log("Answer:", q.answer);
    console.log("-----------");
});
