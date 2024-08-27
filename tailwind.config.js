/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/templates/**/*.{html,js}"],
  theme: {
    extend: {
      colors:{
        'blue-1': '#04ADBF',
        'blue-2': '#04BFBF',
        'green-3': '#025959',
        'green-4': '#A0A603',
        'vanilla-5': '#F2E0C9',
      },
    },
  },
  plugins: [
    require('daisyui'),
  ],
}

