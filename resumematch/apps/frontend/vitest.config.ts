import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['src/**/*.{test,spec}.ts?(x)'],
    coverage: {
      reporter: ['text', 'html'],
    },
  },
})