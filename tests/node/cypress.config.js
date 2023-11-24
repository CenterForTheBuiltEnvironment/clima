const { defineConfig } = require("cypress");

module.exports = defineConfig({
  defaultCommandTimeout: 30 * 1000,
  video: true,
  videoCompression: true,
  e2e: {
    setupNodeEvents(on, config) {
      // implement node event listeners here
    }
  },
});
