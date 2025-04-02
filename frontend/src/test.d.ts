/// <reference types="vitest" />
/// <reference types="@testing-library/jest-dom" />

declare namespace Vi {
  interface Assertion extends jest.Matchers<void, any> {}
  interface AsymmetricMatchersContaining extends jest.Matchers<void, any> {}
}
