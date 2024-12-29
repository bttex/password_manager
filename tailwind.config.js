/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './passwords/templates/**/*.html',
    './passwords/static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"], // temas que serão disponíveis
  }
}

