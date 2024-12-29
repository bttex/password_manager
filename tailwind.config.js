/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './passwords/templates/**/*.html',
    './templates/**/*.html',  // caso tenha templates na raiz
    './passwords/static/**/*.js',
    './static/**/*.js',
    './static/js/**/*.js', 
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"]
  }
}