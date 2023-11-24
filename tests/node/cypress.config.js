const { defineConfig } = require("cypress");

module.exports = defineConfig({
  defaultCommandTimeout: 30 * 1000,
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    }
  },
});
