import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        lava: {
          DEFAULT: "#F56E0F",
          50: "#FEF7F0",
          100: "#FDE6D1",
          200: "#FBCDA3",
          300: "#F9B475",
          400: "#F79B47",
          500: "#F56E0F",
          600: "#E55A0C",
          700: "#B8460A",
          800: "#8B3207",
          900: "#5E1E05",
        },
        snow: {
          DEFAULT: "#FBFBFB",
          50: "#FEFEFE",
          100: "#FDFDFD",
          200: "#FBFBFB",
          300: "#F8F8F8",
          400: "#F5F5F5",
          500: "#F2F2F2",
          600: "#E8E8E8",
          700: "#D6D6D6",
          800: "#C4C4C4",
          900: "#B2B2B2",
        },
        dustyGray: "#878787",
        darkVoid: "#151419",
      },
    },
  },
  plugins: [],
}

export default config
