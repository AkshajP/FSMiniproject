/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./teachers/templates/**/*.html",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("flowbite/plugin")],
};
