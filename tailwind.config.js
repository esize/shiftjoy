
let projectPaths = [
  './teams/templates/**/*.html',
  './employees/templates/**/*.html',
  './forecast/templates/**/*.html',
  './schedules/templates/**/*.html',
  './templates/**/*.html'
  // Add paths to other apps if necessary
]

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: projectPaths,
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
};
