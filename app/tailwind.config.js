/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        main: "#1E4A68",
        accent: "#E3D8DF",
        hover: "#748EA0",
        headerColor: "#23556B",
        textColor: "#050F17",
      },
    },
  },
};
