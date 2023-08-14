/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        bodybg: "#25294a",
        cardbg: "#202442",
        chatbg: "#2D325A",
        iconfill: "#919bc3",
        hovericonfill: "#E9EBF9",
        textcolor: "#919bc3",
        hovertextcolor: "#E9EBF9"
      },
    },
  },
  plugins: [],
};
