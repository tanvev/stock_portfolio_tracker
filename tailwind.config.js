/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',       // Django templates
    './**/templates/**/*.html',    // If using apps
    './static/js/**/*.js',         // If JS files contain Tailwind classes
  ],
  darkMode: 'class',               // Enable dark mode using class strategy
  theme: {
    extend: {},
  },
  plugins: [],
};
